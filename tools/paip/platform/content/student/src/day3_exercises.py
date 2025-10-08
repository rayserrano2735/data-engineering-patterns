"""
Day 3 Exercises: Comprehensions
Exercises 6-9 focus on list/dict comprehensions
"""

from week1_exercises import (
    exercise_1_6,
    exercise_1_7,
    exercise_1_8,
    exercise_1_9
)

__all__ = ['exercise_1_6', 'exercise_1_7', 'exercise_1_8', 'exercise_1_9']

if __name__ == '__main__':
    print("Day 3 Exercises: Comprehensions")
    print("=" * 50)
    for i in range(6, 10):
        print(f"\nExercise 1.{i}:")
        print(eval(f'exercise_1_{i}()'))
