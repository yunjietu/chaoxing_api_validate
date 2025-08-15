#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 https://api.daka1.com/api/validate 接口
"""

import requests
import json
import time
from datetime import datetime

def test_daka1_validate_api():
    """测试 daka1.com 的滑块验证码接口"""
    
    api_url = "https://api.daka1.com/api/validate"
    
    print("=== 测试 daka1.com 滑块验证码接口 ===")
    print(f"接口地址: {api_url}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    try:
        # 设置请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        }
        
        # 记录开始时间
        start_time = time.time()
        
        # 发送GET请求
        print("正在调用接口...")
        response = requests.get(api_url, headers=headers, timeout=30)
        
        # 记录结束时间
        end_time = time.time()
        request_time = end_time - start_time
        
        print(f"请求耗时: {request_time:.2f}秒")
        print(f"HTTP状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        # 检查HTTP状态码
        if response.status_code == 200:
            print("✅ HTTP请求成功")
            
            try:
                # 解析JSON响应
                result = response.json()
                
                print("\n=== 响应内容 ===")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                
                # 分析响应结构
                print("\n=== 响应分析 ===")
                
                if "status" in result:
                    status = result["status"]
                    print(f"状态码: {status}")
                    
                    if status == 0:
                        print("✅ 验证成功")
                        
                        if "data" in result and result["data"]:
                            if "validate" in result["data"]:
                                validate_value = result["data"]["validate"]
                                print(f"✅ 获取到validate值: {validate_value}")
                                
                                # 验证validate格式
                                if validate_value.startswith("validate_"):
                                    print("✅ validate格式正确")
                                else:
                                    print("⚠️ validate格式可能不正确")
                            else:
                                print("❌ 响应中缺少validate字段")
                        else:
                            print("❌ 响应中缺少data字段或data为空")
                    else:
                        print("❌ 验证失败")
                        
                        if "msg" in result:
                            print(f"错误信息: {result['msg']}")
                else:
                    print("❌ 响应中缺少status字段")
                    
                if "msg" in result:
                    print(f"消息: {result['msg']}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应内容: {response.text}")
                
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误")
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def test_multiple_calls():
    """测试多次调用接口"""
    
    print("\n" + "=" * 60)
    print("=== 测试多次调用接口 ===")
    
    api_url = "https://api.daka1.com/api/validate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    success_count = 0
    total_count = 3
    
    for i in range(total_count):
        print(f"\n--- 第 {i+1} 次调用 ---")
        try:
            start_time = time.time()
            response = requests.get(api_url, headers=headers, timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == 0 and result.get("data", {}).get("validate"):
                    success_count += 1
                    print(f"✅ 成功 (耗时: {end_time - start_time:.2f}秒)")
                    print(f"Validate: {result['data']['validate'][:30]}...")
                else:
                    print(f"❌ 失败: {result.get('msg', '未知错误')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 异常: {e}")
        
        # 间隔1秒再调用
        if i < total_count - 1:
            time.sleep(1)
    
    print(f"\n=== 测试总结 ===")
    print(f"总调用次数: {total_count}")
    print(f"成功次数: {success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")

def test_validate_format():
    """测试validate值的格式"""
    
    print("\n" + "=" * 60)
    print("=== 测试validate值格式 ===")
    
    api_url = "https://api.daka1.com/api/validate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == 0 and result.get("data", {}).get("validate"):
                validate_value = result["data"]["validate"]
                
                print(f"完整validate值: {validate_value}")
                print(f"长度: {len(validate_value)}")
                
                # 分析validate格式
                parts = validate_value.split("_")
                if len(parts) >= 2:
                    print(f"前缀: {parts[0]}")
                    print(f"ID部分: {parts[1]}")
                    if len(parts) >= 3:
                        print(f"哈希部分: {parts[2]}")
                        print(f"哈希长度: {len(parts[2])}")
                        
                        # 检查哈希格式（通常是32位十六进制）
                        if len(parts[2]) == 32 and all(c in '0123456789ABCDEF' for c in parts[2].upper()):
                            print("✅ 哈希格式正确（32位十六进制）")
                        else:
                            print("⚠️ 哈希格式可能不正确")
                else:
                    print("⚠️ validate格式不符合预期")
                    
            else:
                print("❌ 未获取到有效的validate值")
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("daka1.com 滑块验证码接口测试工具")
    print("=" * 60)
    
    # 基本功能测试
    test_daka1_validate_api()
    
    # 多次调用测试
    test_multiple_calls()
    
    # validate格式测试
    test_validate_format()
    
    print("\n" + "=" * 60)
    print("测试完成！")
