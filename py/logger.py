"""
    用于创建日志生成器
    需要在logger_config.json中配置输出日志路径，日志等级（可选）
"""
import logging
import functools



log_level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.info,
    'WARNING': logging.warning,
    'ERROR': logging.error,
    'CRITICAL': logging.critical
}

def log_config_parser(config_file_path='conf/logger_config.json'):


    #使用方法，调用时给出日志配置文件路径

    import json, os
    if not os.path.isfile(config_file_path): return None
    with open(config_file_path, 'r') as f:
        data = json.load(f)
    return data
    


def get_logger(name='default_app_name', log_level=logging.DEBUG, output_path='py_logger.log'):

    # 读取配置
    config = log_config_parser()
    if config:
        name = config['name']
        output_path = config['output_path']
        log_level = log_level_map[config['log_level']]
    # 创建并配置日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 创建并添加控制台输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 创建并添加文件输出处理器
    file_handler = logging.FileHandler(output_path)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger



def log_function_call(logger):
    """
        日志装饰器，用于调用函数时，将函数调用名称、参数、开始结束时间写入日志
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 记录函数名，参数
            f_name = func.__name__
            f_args = ', '.join([f'{key}={value}' for key, value in kwargs.items()])
            if args:
                f_args += ', '.join([str(arg) for arg in args])
           
            # run func
            result = func(*args, **kwargs)

            
            # 记录日志
            logger.debug(f"Start call Function '{f_name}' ")
            logger.debug(f"Function '{f_name}' called with args: {f_args}")
            logger.debug(f"End call Function '{f_name}' ")
            
            return result
        
        return wrapper
    return decorator
    
logger = get_logger(name='self_test')

if __name__ == '__main__':
    #logger = get_logger(name='self_test')
    # 输出日志信息
    logger.debug('这是一个调试信息')
    logger.info('这是一个普通信息')
    logger.warning('这是一个警告信息')
    logger.error('这是一个错误信息')
    logger.critical('这是一个严重错误信息')
    @log_function_call(logger)
    def f():
        print('hello')
        
    f()

