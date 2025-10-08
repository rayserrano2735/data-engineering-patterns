"""
Day 5 Exercises: Lambda and Sorting
Exercises 14-16 focus on lambda expressions and sorting
"""

from week1_exercises import (
    exercise_1_14,
    exercise_1_15,
    exercise_1_16
)

__all__ = ['exercise_1_14', 'exercise_1_15', 'exercise_1_16']

if __name__ == '__main__':
    print("Day 5 Exercises: Lambda and Sorting")
    print("=" * 50)
    for i in range(14, 17):
        print(f"\nExercise 1.{i}:")
        print(eval(f'exercise_1_{i}()'))
