# -*- coding: utf-8 -*-
"""
多进程狼人杀游戏胜率测试
"""
import asyncio
import multiprocessing as mp
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ProcessPoolExecutor
from main_new import main


def run_single_game(game_id: int) -> tuple:
    """运行单局游戏"""
    try:

        import random
        delay = random.uniform(0, 2)  # 0-2秒随机延迟
        time.sleep(delay)
        
        start_time = time.time()
        result = asyncio.run(main())
        duration = time.time() - start_time
        return game_id, result, duration, ""
    except Exception as e:
        print(e)
        duration = time.time() - start_time
        return game_id, None, duration, str(e)


def test_games(num_games: int = 100, num_processes: int = None):
    """多进程测试游戏胜率"""
    if num_processes is None:
        num_processes = min(mp.cpu_count(), num_games)
    
    print(f"开始测试 {num_games} 局游戏，使用 {num_processes} 个进程...")
    
    start_time = time.time()
    results = []
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(run_single_game, i) for i in range(num_games)]
        
        for i, future in enumerate(futures):
            result = future.result()
            results.append(result)
            if (i + 1) % 10 == 0:
                print(f"已完成 {i + 1}/{num_games} 局游戏")
    
    # 统计结果
    valid_results = [r for r in results if r[1] is not None]
    wolf_wins = sum(1 for r in valid_results if r[1] is True)
    village_wins = sum(1 for r in valid_results if r[1] is False)
    
    total_time = time.time() - start_time
    
    print(f"\n测试完成！")
    print(f"总游戏数: {num_games}")
    print(f"有效游戏数: {len(valid_results)}")
    print(f"狼人获胜: {wolf_wins} 局 ({wolf_wins/len(valid_results)*100:.1f}%)")
    print(f"好人获胜: {village_wins} 局 ({village_wins/len(valid_results)*100:.1f}%)")
    print(f"总耗时: {total_time:.1f} 秒")

    with open("results_deepwerewolf-32b_wolf.txt",'w',encoding='utf-8') as f:
        f.write(f"总游戏数: {num_games}\n")
        f.write(f"有效游戏数: {len(valid_results)}\n")
        f.write(f"狼人获胜: {wolf_wins} 局 ({wolf_wins/len(valid_results)*100:.1f}%) \n")
        f.write(f"好人获胜: {village_wins} 局 ({village_wins/len(valid_results)*100:.1f}%) \n")
        f.write(f"总耗时: {total_time:.1f} 秒\n")


if __name__ == "__main__":
    test_games(50)
