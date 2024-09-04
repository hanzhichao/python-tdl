from pprint import pprint

import pytest

from python_tdl import Env, Step, TestCase, TestSuite


@pytest.fixture
def env():
    env = Env('test', config={'Http': {'base_url': 'http://postman-echo.com'}})
    return env


@pytest.fixture
def context(env):
    return env.context


def test_step(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
            "set": {"url": "$result.url"},
            "verify": [
                {"eq": ["$result.status_code", 200]},
                {"eq": ["$url", "http://postman-echo.com/get?a=1&b=2&c=3"]},
                {"contains": ["$result.url", "http://postman-echo.com/get"]},

            ]}
    step = Step.load(data)
    print('\nStep --------------------------------')
    pprint(step.__dict__)
    result = step.run(context)
    print('\nContext --------------------------------')
    pprint(context.variables)
    print('\nResult --------------------------------')
    pprint(result.data)


def test_step_skip(context):
    data = {"method": "Http.get",
            "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
            "skip": [2 > 1, '跳过吧']
            }
    step = Step.load(data)
    print('\nStep --------------------------------')
    pprint(step.__dict__)
    result = step.run(context)
    print('\nContext --------------------------------')
    pprint(context.variables)
    print('\nResult --------------------------------')
    pprint(result.data)


def test_testcase(env):
    data = {
        "name": "test_api_demo",
        "description": "test description",
        "priority": 1,
        "tags": ["http", "api-test"],
        "timeout": 100,
        "setups": [
            {"name": "测试准备", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}
        ],
        "teardowns": [
            {"name": "测试清理", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}}
        ],
        "steps": [
            {"name": "步骤1", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
            {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
            {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
             "set": {"url": "$.url"}, "verify": [{"eq": ["$url", "/get"]}]}
        ]
    }
    testcase = TestCase.load(data)
    print()
    pprint(testcase.__dict__)
    result = testcase.run(env)
    print('\nResult --------------------------------')
    pprint(result.data)


def test_testcase_with_data(env):
    data = {
        "name": "数据驱动测试",
        "data": [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6},
            {'a': 7, 'b': 8, 'c': 9},

        ],
        "steps": [
            {"name": "步骤1", "method": "Http.get", "args": {"url": "/get", "params": {"a": '$a', "b": '$b', "c": '$c'}}},
        ]
    }
    testcase = TestCase.load(data)
    print()
    pprint(testcase.__dict__)
    results = testcase.run(env)
    print('\nResult --------------------------------')
    pprint([result.data for result in results])


def test_test_suite(env):
    data = {
        "name": "testsuite_01",
        "description": "testsuite description",
        "tags": ["api-test"],
        "priority": 1,
        "setups": [],
        "teardowns": [],
        "suite_steps": [],
        "suite_teardowns": [],
        "tests": [
            {
                "name": "test_api_demo_1",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                    {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
                     "set": {"url": "$.url"}, "verify": [{"eq": ["$url", "/get"]}]}
                ]
            },
            {
                "name": "test_api_demo_2",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                ]
            }
        ]
    }

    testsuite = TestSuite.load(data)
    # print(testsuite.__dict__)
    result = testsuite.run(env)
    print()
    pprint(result.data)
