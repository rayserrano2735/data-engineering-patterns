#!/usr/bin/env python3
"""
Diary Compression System with Parameters
- Works with curated diary chapters (post-curation)
- All settings via parameters file or command line
- Learns from existing chapters to compress new ones
"""

import re
import os
import sys
import json
import hashlib
import argparse
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter, defaultdict
from datetime import datetime
import math


class CorpusAnalyzer:
    """Analyzes curated diary chapters to generate optimal compression rules."""
    
    def __init__(self, params: Dict = None):
        """Initialize with parameters."""
        self.params = params or {}
        self.min_phrase_length = self.params.get('min_phrase_length', 2)
        self.min_phrase_freq = self.params.get('min_phrase_freq', 3)
        self.max_symbols = self.params.get('max_symbols', 50)
        self.max_two_letter_codes = self.params.get('max_two_letter_codes', 100)
        self.max_phrase_codes = self.params.get('max_phrase_codes', 200)
    
    def analyze_diary(self, diary_folder: str, output_config: str = None) -> Dict:
        """
        Analyze curated diary chapters to generate compression rules.
        
        Args:
            diary_folder: Folder containing curated chapter files
            output_config: Path for output configuration (optional)
        
        Returns:
            Generated compression configuration
        """
        if output_config is None:
            output_config = os.path.join(diary_folder, 'compression_config.json')
        
        # Find all chapter files
        chapter_files = self._find_chapter_files(diary_folder)
        
        if not chapter_files:
            print(f"No chapter files found in {diary_folder}")
            return None
        
        print(f"\n{'='*70}")
        print(f"ANALYZING DIARY CORPUS")
        print(f"{'='*70}")
        print(f"Diary folder: {diary_folder}")
        print(f"Chapters found: {len(chapter_files)}")
        
        # Analyze all chapters
        config = self._analyze_chapters(chapter_files)
        
        if config:
            # Add diary metadata
            config['diary_metadata'] = {
                'diary_folder': diary_folder,
                'chapters_analyzed': len(chapter_files),
                'chapter_files': [os.path.basename(f) for f in chapter_files],
                'analysis_date': datetime.now().isoformat()
            }
            
            # Save configuration
            with open(output_config, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"\n{'='*70}")
            print(f"ANALYSIS COMPLETE")
            print(f"{'='*70}")
            print(f"Configuration saved: {output_config}")
            print(f"Unique words found: {len(config.get('symbol_mappings', {})) + len(config.get('two_letter_codes', {})):,}")
            print(f"Phrase patterns: {len(config.get('phrase_mappings', {})):,}")
            print(f"Compression potential: ~{config.get('estimated_compression', 'N/A')}")
        
        return config
    
    def _find_chapter_files(self, diary_folder: str) -> List[str]:
        """Find all chapter files in the diary folder."""
        chapter_files = []
        patterns = self.params.get('chapter_patterns', ['chapter*.txt', 'chapter*.md', 'diary*.txt'])
        extensions = self.params.get('file_extensions', ['.txt', '.md'])
        
        for file in sorted(os.listdir(diary_folder)):
            filepath = os.path.join(diary_folder, file)
            if os.path.isfile(filepath):
                # Check if matches any pattern
                for pattern in patterns:
                    if self._matches_pattern(file, pattern):
                        chapter_files.append(filepath)
                        break
                # Or check extensions
                elif any(file.endswith(ext) for ext in extensions):
                    chapter_files.append(filepath)
        
        return sorted(chapter_files)
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches a pattern (supports * wildcards)."""
        import fnmatch
        return fnmatch.fnmatch(filename.lower(), pattern.lower())
    
    def _analyze_chapters(self, chapter_files: List[str]) -> Dict:
        """Analyze chapter files to generate compression configuration."""
        # Aggregated statistics
        word_freq = Counter()
        phrase_freq = Counter()
        sentence_patterns = Counter()
        bigram_freq = Counter()
        
        total_chars = 0
        total_messages = 0
        
        for i, filepath in enumerate(chapter_files, 1):
            print(f"  Analyzing chapter {i}/{len(chapter_files)}: {os.path.basename(filepath)}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                    if not text.strip():
                        continue
                    
                    total_chars += len(text)
                    
                    # Extract words
                    words = re.findall(r'\b\w+\b', text.lower())
                    word_freq.update(words)
                    
                    # Extract phrases (2-5 words)
                    for n in range(self.min_phrase_length, 6):
                        for i in range(len(words) - n + 1):
                            phrase = ' '.join(words[i:i+n])
                            phrase_freq[phrase] += 1
                    
                    # Extract sentence patterns
                    sentences = re.split(r'[.!?]+', text)
                    for sent in sentences:
                        sent_words = sent.strip().split()[:4]
                        if len(sent_words) >= 2:
                            pattern = ' '.join(sent_words)
                            sentence_patterns[pattern] += 1
                    
                    # Character-level patterns
                    clean_text = re.sub(r'\s+', '', text.lower())
                    for i in range(len(clean_text) - 1):
                        bigram_freq[clean_text[i:i+2]] += 1
                    
                    total_messages += len(sentences)
                    
            except Exception as e:
                print(f"    Warning: Error processing {filepath}: {e}")
                continue
        
        # Generate optimized compression configuration
        config = self._generate_optimized_config(
            word_freq, phrase_freq, sentence_patterns, bigram_freq,
            total_chars, total_messages
        )
        
        return config
    
    def _generate_optimized_config(self, word_freq, phrase_freq, sentence_patterns, 
                                  bigram_freq, total_chars, total_messages) -> Dict:
        """Generate optimized compression configuration from statistics."""
        
        # Calculate compression potential
        total_words = sum(word_freq.values())
        top_100_words_freq = sum(freq for _, freq in word_freq.most_common(100))
        compression_potential = (top_100_words_freq / total_words) * 100 if total_words > 0 else 0
        
        config = {
            'version': '2.0',
            'generated': datetime.now().isoformat(),
            'corpus_stats': {
                'total_chars': total_chars,
                'total_messages': total_messages,
                'unique_words': len(word_freq),
                'total_words': total_words,
                'compression_potential': f"{compression_potential:.1f}%"
            },
            
            # Symbol mappings for ultra-common words
            'symbol_mappings': self._generate_symbol_mappings(word_freq),
            
            # Two-letter codes for very common words  
            'two_letter_codes': self._generate_two_letter_codes(word_freq),
            
            # Phrase compressions
            'phrase_mappings': self._generate_phrase_mappings(phrase_freq),
            
            # Sentence patterns
            'sentence_patterns': self._generate_sentence_patterns(sentence_patterns),
            
            # Suffix mappings
            'suffix_mappings': self._generate_suffix_mappings(word_freq),
            
            # Parameters
            'compression_params': self.params.get('compression_params', {
                'min_word_length_for_vowel_removal': 5,
                'aggressive_vowel_removal': True,
                'track_topics': True,
                'track_entities': True,
                'compress_whitespace': True,
                'compress_numbers': True
            }),
            
            'estimated_compression': f"{min(75 + compression_potential/4, 85):.0f}%"
        }
        
        return config
    
    def _generate_symbol_mappings(self, word_freq: Counter) -> Dict[str, str]:
        """Generate single-symbol mappings for most frequent words."""
        symbols = ['§', '@', '#', '◊', '◈', '◉', '†', '‡', '°', '±', '∞', '≈', '≠', '≤', '≥',
                  'α', 'β', 'γ', 'δ', 'ε', 'θ', 'λ', 'μ', 'π', 'σ', 'φ', 'ω', 'Ω', 'Δ', 'Σ',
                  '¤', '¢', '£', '¥', '€', '₹', '¿', '¡', '«', '»', '‹', '›']
        
        mappings = {}
        for word, _ in word_freq.most_common(min(self.max_symbols, len(symbols))):
            if len(word) > 2 and symbols:
                mappings[word] = symbols.pop(0)
        
        return mappings
    
    def _generate_two_letter_codes(self, word_freq: Counter) -> Dict[str, str]:
        """Generate two-letter codes for common words."""
        chars1 = 'QXZJK'
        chars2 = 'QXZJKVWYBFGPD'
        
        codes = [c1 + c2 for c1 in chars1 for c2 in chars2]
        
        mappings = {}
        start_idx = len(self._generate_symbol_mappings(word_freq))
        
        for word, _ in word_freq.most_common(start_idx + self.max_two_letter_codes)[start_idx:]:
            if len(word) > 3 and codes:
                mappings[word] = codes.pop(0)
        
        return mappings
    
    def _generate_phrase_mappings(self, phrase_freq: Counter) -> Dict[str, str]:
        """Generate mappings for common phrases."""
        mappings = {}
        prefixes = {'?': 1, '!': 1, '~': 1, '&': 1, '*': 1}
        
        for phrase, freq in phrase_freq.most_common(self.max_phrase_codes):
            if freq >= self.min_phrase_freq:
                words = phrase.split()
                # Assign prefix based on first word
                if words[0] in ['can', 'could', 'would', 'should', 'will', 'what', 'how', 'why']:
                    prefix = '?'
                elif words[0] in ['i', "i'm", "i've", "i'll", "i'd"]:
                    prefix = '!'
                elif words[0] in ['the', 'this', 'that', 'these', 'those']:
                    prefix = '&'
                else:
                    prefix = '~'
                
                if prefixes[prefix] < 100:
                    mappings[phrase] = f"{prefix}{prefixes[prefix]}"
                    prefixes[prefix] += 1
        
        return mappings
    
    def _generate_sentence_patterns(self, patterns: Counter) -> List[str]:
        """Identify common sentence starters."""
        return [pattern for pattern, freq in patterns.most_common(20) if freq > 3]
    
    def _generate_suffix_mappings(self, word_freq: Counter) -> Dict[str, str]:
        """Generate suffix compression mappings."""
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ation', 'ment',
                   'ness', 'able', 'ible', 'ful', 'less', 'ity', 'ive', 'ous']
        
        suffix_codes = ['₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉', '₀',
                       '₊', '₋', '₌', '₍', '₎', '⁺', '⁻', '⁼']
        
        # Count suffix frequencies
        suffix_freq = Counter()
        for word, freq in word_freq.items():
            for suffix in suffixes:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    suffix_freq[suffix] += freq
        
        # Assign codes to most common suffixes
        mappings = {}
        for suffix, _ in suffix_freq.most_common(len(suffix_codes)):
            if suffix_codes:
                mappings[suffix] = suffix_codes.pop(0)
        
        return mappings


class CompressionEngine:
    """Compression engine that uses configuration to compress diary chapters."""
    
    def __init__(self, config: Dict = None, config_path: str = None):
        """Initialize with configuration."""
        if config:
            self.config = config
        elif config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self._get_default_config()
        
        self.reset_session()
    
    def reset_session(self):
        """Reset session-specific state."""
        self.topic_refs = {}
        self.entity_refs = {}
        self.repeated_blocks = {}
        self.custom_abbrevs = {}
        self.stats = {'topics': 0, 'entities': 0, 'blocks': 0}
    
    def compress_diary(self, input_folder: str, output_folder: str = None,
                      specific_files: List[str] = None) -> Dict:
        """
        Compress diary chapters using loaded configuration.
        
        Args:
            input_folder: Folder containing curated chapters to compress
            output_folder: Output folder (default: input_folder + '_compressed')
            specific_files: Optional list of specific files to compress
        
        Returns:
            Compression results dictionary
        """
        if output_folder is None:
            output_folder = input_folder + '_compressed'
        
        os.makedirs(output_folder, exist_ok=True)
        
        # Determine files to compress
        if specific_files:
            files_to_compress = [os.path.join(input_folder, f) for f in specific_files]
        else:
            files_to_compress = []
            for file in sorted(os.listdir(input_folder)):
                filepath = os.path.join(input_folder, file)
                if os.path.isfile(filepath) and file.endswith(('.txt', '.md')):
                    files_to_compress.append(filepath)
        
        if not files_to_compress:
            print(f"No files to compress in {input_folder}")
            return {}
        
        print(f"\n{'='*70}")
        print(f"COMPRESSING DIARY CHAPTERS")
        print(f"{'='*70}")
        print(f"Input folder: {input_folder}")
        print(f"Output folder: {output_folder}")
        print(f"Files to compress: {len(files_to_compress)}")
        
        # Master results
        results = {
            'compression_date': datetime.now().isoformat(),
            'config_version': self.config.get('version', 'unknown'),
            'input_folder': input_folder,
            'output_folder': output_folder,
            'files': [],
            'total_stats': {}
        }
        
        total_original = 0
        total_compressed = 0
        
        for filepath in files_to_compress:
            filename = os.path.basename(filepath)
            print(f"\nCompressing: {filename}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    original_text = f.read()
                
                if not original_text.strip():
                    print(f"  Skipping empty file")
                    continue
                
                # Reset session for each file
                self.reset_session()
                
                # Compress
                compressed_text, decompression_key = self._compress_text(original_text, filename)
                
                # Save compressed file
                output_path = os.path.join(output_folder, filename.replace('.txt', '.cmp.txt').replace('.md', '.cmp.md'))
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(compressed_text)
                
                # Save decompression key
                key_path = output_path + '.key.json'
                with open(key_path, 'w', encoding='utf-8') as f:
                    json.dump(decompression_key, f, indent=2, ensure_ascii=False)
                
                # Track results
                original_size = len(original_text)
                compressed_size = len(compressed_text)
                ratio = (1 - compressed_size/original_size) * 100
                
                file_result = {
                    'filename': filename,
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'compression_ratio': f"{ratio:.1f}%",
                    'topics_tracked': self.stats['topics'],
                    'entities_tracked': self.stats['entities'],
                    'blocks_compressed': self.stats['blocks']
                }
                
                results['files'].append(file_result)
                total_original += original_size
                total_compressed += compressed_size
                
                print(f"  Original: {original_size:,} chars")
                print(f"  Compressed: {compressed_size:,} chars")
                print(f"  Ratio: {ratio:.1f}%")
                print(f"  Topics/Entities/Blocks: {self.stats['topics']}/{self.stats['entities']}/{self.stats['blocks']}")
                
            except Exception as e:
                print(f"  Error: {e}")
                results['files'].append({
                    'filename': filename,
                    'error': str(e)
                })
        
        # Calculate total statistics
        if total_original > 0:
            total_ratio = (1 - total_compressed/total_original) * 100
            results['total_stats'] = {
                'files_compressed': len([f for f in results['files'] if 'error' not in f]),
                'total_original_size': total_original,
                'total_compressed_size': total_compressed,
                'overall_compression_ratio': f"{total_ratio:.1f}%"
            }
            
            # Save master results
            results_path = os.path.join(output_folder, '_compression_results.json')
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n{'='*70}")
            print(f"COMPRESSION COMPLETE")
            print(f"{'='*70}")
            print(f"Files compressed: {results['total_stats']['files_compressed']}")
            print(f"Overall compression: {total_ratio:.1f}%")
            print(f"Results saved: {results_path}")
        
        return results
    
    def _compress_text(self, text: str, filename: str) -> Tuple[str, Dict]:
        """Compress text using configuration."""
        original_length = len(text)
        compressed = text
        
        # Apply compressions in order
        compressed = self._apply_phrase_compression(compressed)
        compressed = self._apply_word_compression(compressed)
        compressed = self._apply_suffix_compression(compressed)
        compressed = self._track_and_compress_entities(compressed)
        compressed = self._compress_repeated_blocks(compressed)
        
        if self.config.get('compression_params', {}).get('compress_whitespace', True):
            compressed = self._compress_whitespace(compressed)
        
        # Create decompression key
        decompression_key = {
            'version': self.config.get('version', '2.0'),
            'filename': filename,
            'compression_date': datetime.now().isoformat(),
            'mappings': {
                'symbols': {v: k for k, v in self.config.get('symbol_mappings', {}).items()},
                'two_letter': {v: k for k, v in self.config.get('two_letter_codes', {}).items()},
                'phrases': {v: k for k, v in self.config.get('phrase_mappings', {}).items()},
                'suffixes': {v: k for k, v in self.config.get('suffix_mappings', {}).items()},
                'topics': {v: k for k, v in self.topic_refs.items()},
                'entities': {v: k for k, v in self.entity_refs.items()},
                'blocks': self.repeated_blocks,
                'custom': {v: k for k, v in self.custom_abbrevs.items()}
            },
            'stats': {
                'original_length': original_length,
                'compressed_length': len(compressed),
                'compression_ratio': f"{(1 - len(compressed)/original_length)*100:.1f}%"
            }
        }
        
        # Add header
        hash_id = hashlib.md5(filename.encode()).hexdigest()[:8]
        compressed = f"[DIARY:{hash_id}]\n{compressed}"
        
        return compressed, decompression_key
    
    def _apply_phrase_compression(self, text: str) -> str:
        """Apply phrase-level compression."""
        for phrase, code in sorted(self.config.get('phrase_mappings', {}).items(), 
                                  key=lambda x: -len(x[0])):
            text = re.sub(re.escape(phrase), code, text, flags=re.IGNORECASE)
        return text
    
    def _apply_word_compression(self, text: str) -> str:
        """Apply word-level compression."""
        words = re.findall(r'\b\w+\b|\W+', text)
        compressed_words = []
        
        for word in words:
            if word.isalpha():
                word_lower = word.lower()
                
                # Check mappings
                if word_lower in self.config.get('symbol_mappings', {}):
                    compressed_words.append(self.config['symbol_mappings'][word_lower])
                elif word_lower in self.config.get('two_letter_codes', {}):
                    compressed_words.append(self.config['two_letter_codes'][word_lower])
                elif len(word) > 12:
                    # Create custom abbreviation
                    if word_lower not in self.custom_abbrevs:
                        abbrev = f"¤{len(self.custom_abbrevs)+1}"
                        self.custom_abbrevs[word_lower] = abbrev
                    compressed_words.append(self.custom_abbrevs[word_lower])
                elif len(word) >= 5:
                    # Remove vowels
                    compressed_words.append(self._remove_vowels(word))
                else:
                    compressed_words.append(word)
            else:
                compressed_words.append(word)
        
        return ''.join(compressed_words)
    
    def _apply_suffix_compression(self, text: str) -> str:
        """Apply suffix compression."""
        for suffix, code in self.config.get('suffix_mappings', {}).items():
            pattern = re.compile(r'\b(\w{3,})' + re.escape(suffix) + r'\b')
            text = pattern.sub(r'\1' + code, text)
        return text
    
    def _track_and_compress_entities(self, text: str) -> str:
        """Track and compress repeated entities."""
        if not self.config.get('compression_params', {}).get('track_entities', True):
            return text
        
        # Find entities (capitalized words/phrases)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        for entity in entities:
            if entity not in ['The', 'This', 'That', 'These', 'Those']:
                if entity not in self.entity_refs:
                    self.entity_refs[entity] = f"E{len(self.entity_refs)+1}"
                    self.stats['entities'] += 1
                
                # Replace subsequent occurrences
                first_idx = text.find(entity)
                if first_idx >= 0 and text.count(entity) > 1:
                    text = text[:first_idx+len(entity)] + text[first_idx+len(entity):].replace(entity, self.entity_refs[entity])
        
        return text
    
    def _compress_repeated_blocks(self, text: str) -> str:
        """Compress repeated text blocks."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        result = []
        
        for sent in sentences:
            if len(sent) > 50:
                sent_hash = hashlib.md5(sent.strip().lower().encode()).hexdigest()[:6]
                if sent_hash in self.repeated_blocks:
                    result.append(f"[B:{sent_hash}]")
                    self.stats['blocks'] += 1
                else:
                    self.repeated_blocks[sent_hash] = sent.strip()
                    result.append(sent)
            else:
                result.append(sent)
        
        return ' '.join(result)
    
    def _compress_whitespace(self, text: str) -> str:
        """Compress whitespace and punctuation."""
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text
    
    def _remove_vowels(self, word: str) -> str:
        """Remove vowels from word (keep first)."""
        if len(word) < 5:
            return word
        
        result = [word[0]]
        for char in word[1:]:
            if char.lower() not in 'aeiou':
                result.append(char)
        
        return ''.join(result) if len(result) > 1 else word
    
    def _get_default_config(self) -> Dict:
        """Return minimal default configuration."""
        return {
            'version': 'default',
            'symbol_mappings': {
                'the': '§', 'and': '&', 'you': 'U', 'for': '4'
            },
            'two_letter_codes': {},
            'phrase_mappings': {},
            'suffix_mappings': {
                'ing': '₈', 'ed': '₉', 'tion': '₁'
            },
            'compression_params': {
                'min_word_length_for_vowel_removal': 5,
                'compress_whitespace': True
            }
        }


def load_parameters(param_file: str = None) -> Dict:
    """Load parameters from file or return defaults."""
    if param_file and os.path.exists(param_file):
        with open(param_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Default parameters
    return {
        'diary_folder': 'diary',
        'output_folder': 'diary_compressed',
        'config_file': 'diary_compression_config.json',
        'chapter_patterns': ['chapter*.txt', 'chapter*.md', 'curated*.txt'],
        'file_extensions': ['.txt', '.md'],
        'min_phrase_length': 2,
        'min_phrase_freq': 3,
        'max_symbols': 50,
        'max_two_letter_codes': 100,
        'max_phrase_codes': 200,
        'compression_params': {
            'min_word_length_for_vowel_removal': 5,
            'aggressive_vowel_removal': True,
            'track_topics': True,
            'track_entities': True,
            'compress_whitespace': True,
            'compress_numbers': True
        }
    }


def main():
    """Main entry point with command line arguments."""
    parser = argparse.ArgumentParser(description='Diary Compression System')
    parser.add_argument('command', choices=['analyze', 'compress', 'both'],
                       help='Command to execute: analyze corpus, compress files, or both')
    parser.add_argument('--diary-folder', '-d', default=None,
                       help='Folder containing diary chapters')
    parser.add_argument('--output-folder', '-o', default=None,
                       help='Output folder for compressed files')
    parser.add_argument('--config-file', '-c', default=None,
                       help='Configuration file path')
    parser.add_argument('--params-file', '-p', default='parameters.json',
                       help='Parameters file (default: parameters.json)')
    parser.add_argument('--specific-files', '-f', nargs='+',
                       help='Specific files to compress')
    
    args = parser.parse_args()
    
    # Load parameters
    params = load_parameters(args.params_file)
    
    # Override with command line arguments
    if args.diary_folder:
        params['diary_folder'] = args.diary_folder
    if args.output_folder:
        params['output_folder'] = args.output_folder
    if args.config_file:
        params['config_file'] = args.config_file
    
    print(f"\n{'='*70}")
    print("DIARY COMPRESSION SYSTEM")
    print(f"{'='*70}")
    print(f"Parameters file: {args.params_file}")
    print(f"Diary folder: {params['diary_folder']}")
    print(f"Config file: {params['config_file']}")
    
    # Execute command
    if args.command in ['analyze', 'both']:
        # Analyze diary to generate configuration
        analyzer = CorpusAnalyzer(params)
        config = analyzer.analyze_diary(
            diary_folder=params['diary_folder'],
            output_config=params['config_file']
        )
        
        if not config:
            print("Analysis failed. Exiting.")
            return
    
    if args.command in ['compress', 'both']:
        # Compress using configuration
        if args.command == 'compress' and not os.path.exists(params['config_file']):
            print(f"Configuration file not found: {params['config_file']}")
            print("Run 'analyze' first to generate configuration.")
            return
        
        engine = CompressionEngine(config_path=params['config_file'])
        results = engine.compress_diary(
            input_folder=params['diary_folder'],
            output_folder=params['output_folder'],
            specific_files=args.specific_files
        )
    
    print(f"\n{'='*70}")
    print("COMPLETE")
    print(f"{'='*70}")


def create_sample_parameters_file():
    """Create a sample parameters.json file."""
    params = {
        "diary_folder": "diary",
        "output_folder": "diary_compressed",
        "config_file": "diary_compression_config.json",
        "chapter_patterns": [
            "chapter*.txt",
            "chapter*.md",
            "curated*.txt",
            "diary*.txt"
        ],
        "file_extensions": [".txt", ".md"],
        "min_phrase_length": 2,
        "min_phrase_freq": 3,
        "max_symbols": 50,
        "max_two_letter_codes": 100,
        "max_phrase_codes": 200,
        "compression_params": {
            "min_word_length_for_vowel_removal": 5,
            "aggressive_vowel_removal": true,
            "track_topics": true,
            "track_entities": true,
            "compress_whitespace": true,
            "compress_numbers": true
        }
    }
    
    with open('parameters.json', 'w', encoding='utf-8') as f:
        json.dump(params, f, indent=2, ensure_ascii=False)
    
    print("Created parameters.json file with default settings.")
    print("Edit this file to customize compression behavior.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # No arguments - show help
        print("Usage: python diary_compressor.py [command] [options]")
        print("\nCommands:")
        print("  analyze    - Analyze diary corpus to generate compression config")
        print("  compress   - Compress diary chapters using existing config")
        print("  both       - Analyze then compress")
        print("\nOptions:")
        print("  --diary-folder, -d   : Diary folder path")
        print("  --output-folder, -o  : Output folder path")
        print("  --config-file, -c    : Configuration file path")
        print("  --params-file, -p    : Parameters file (default: parameters.json)")
        print("  --specific-files, -f : Specific files to compress")
        print("\nExample:")
        print("  python diary_compressor.py both -d diary -o compressed")
        print("\nTo create a sample parameters file:")
        print("  python diary_compressor.py --create-params")
        
        if '--create-params' in sys.argv:
            create_sample_parameters_file()
    else:
        main()
