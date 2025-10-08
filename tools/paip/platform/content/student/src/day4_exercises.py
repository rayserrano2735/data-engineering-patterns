"""
Day 4 Exercises: Functions and Parameters
Exercises 10-13 focus on function definition and usage
"""

from week1_exercises import (
    exercise_1_10,
    exercise_1_11,
    exercise_1_12,
    exercise_1_13
)

__all__ = ['exercise_1_10', 'exercise_1_11', 'exercise_1_12', 'exercise_1_13']

if __name__ == '__main__':
    print("Day 4 Exercises: Functions and Parameters")
    print("=" * 50)
    for i in range(10, 14):
        print(f"\nExercise 1.{i}:")
        print(eval(f'exercise_1_{i}()'))
