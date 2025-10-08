"""
Day 6 Exercises: String Operations
Exercises 17-19 focus on string manipulation
"""

from week1_exercises import (
    exercise_1_17,
    exercise_1_18,
    exercise_1_19
)

__all__ = ['exercise_1_17', 'exercise_1_18', 'exercise_1_19']

if __name__ == '__main__':
    print("Day 6 Exercises: String Operations")
    print("=" * 50)
    for i in range(17, 20):
        print(f"\nExercise 1.{i}:")
        print(eval(f'exercise_1_{i}()'))
