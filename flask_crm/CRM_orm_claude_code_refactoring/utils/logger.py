"""
중앙화된 로깅 설정
"""
import logging
import logging.handlers
import os
from datetime import datetime
from config import Config

def setup_logging(app=None, config=None):
    """
    애플리케이션 로깅 설정
    
    Args:
        app: Flask 애플리케이션 인스턴스
        config: 설정 객체
    """
    if config is None:
        config = Config()
    
    # 로그 레벨 설정
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # 로그 포맷터 설정
    formatter = logging.Formatter(
        fmt=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 기존 핸들러 제거
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 파일 핸들러 (회전 로그)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/crm.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 에러 전용 파일 핸들러
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/error.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Flask 앱이 제공된 경우 Flask 로거도 설정
    if app:
        app.logger.setLevel(log_level)
        
        # Flask의 기본 핸들러 제거
        for handler in app.logger.handlers[:]:
            app.logger.removeHandler(handler)
        
        # 동일한 핸들러 추가
        app.logger.addHandler(console_handler)
        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_handler)
    
    # 서드파티 라이브러리 로그 레벨 조정
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    logging.info("로깅 시스템이 초기화되었습니다.")

def get_logger(name=None):
    """
    로거 인스턴스 반환
    
    Args:
        name: 로거 이름 (기본값: 호출한 모듈명)
    
    Returns:
        logging.Logger: 로거 인스턴스
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    return logging.getLogger(name)

class DatabaseLogHandler(logging.Handler):
    """
    데이터베이스에 로그를 저장하는 핸들러
    (향후 로그 모니터링을 위해 구현)
    """
    
    def __init__(self, db_session=None):
        super().__init__()
        self.db_session = db_session
    
    def emit(self, record):
        """로그 레코드를 데이터베이스에 저장"""
        try:
            if self.db_session:
                # 여기에 로그 테이블에 저장하는 로직 구현
                # 예: LogEntry 모델 생성 후 저장
                pass
        except Exception:
            # 로그 저장 실패 시 무시 (로깅 때문에 앱이 중단되면 안됨)
            pass

def log_function_call(func):
    """
    함수 호출을 로깅하는 데코레이터
    
    Usage:
        @log_function_call
        def my_function(arg1, arg2):
            return result
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # 함수 호출 시작 로그
        logger.debug(f"함수 호출 시작: {func.__name__}")
        
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            
            # 함수 호출 성공 로그
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"함수 호출 완료: {func.__name__} (실행시간: {execution_time:.3f}초)")
            
            return result
            
        except Exception as e:
            # 함수 호출 실패 로그
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"함수 호출 실패: {func.__name__} (실행시간: {execution_time:.3f}초) - {str(e)}")
            raise
    
    return wrapper

def log_database_operation(operation_type):
    """
    데이터베이스 작업을 로깅하는 데코레이터
    
    Args:
        operation_type: 작업 타입 (INSERT, UPDATE, DELETE, SELECT)
    
    Usage:
        @log_database_operation('INSERT')
        def create_user(user_data):
            # 사용자 생성 로직
            pass
    """
    def decorator(func):
        import functools
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            
            logger.info(f"DB 작업 시작: {operation_type} - {func.__name__}")
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"DB 작업 성공: {operation_type} - {func.__name__} (실행시간: {execution_time:.3f}초)")
                return result
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"DB 작업 실패: {operation_type} - {func.__name__} (실행시간: {execution_time:.3f}초) - {str(e)}")
                raise
        
        return wrapper
    return decorator