#!/usr/bin/env python3
"""
Flask CRM 애플리케이션 실행 스크립트
"""
import os
import sys
from app import create_app

def main():
    """메인 실행 함수"""
    # 환경 설정
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # 애플리케이션 생성
    app = create_app(config_name)
    
    # 개발 환경에서만 디버그 모드 활성화
    debug_mode = config_name == 'development'
    
    print(f"Flask CRM 애플리케이션을 {config_name} 모드로 시작합니다...")
    print(f"URL: http://{app.config['HOST']}:{app.config['PORT']}")
    
    # 애플리케이션 실행
    app.run(
        debug=debug_mode,
        host=app.config['HOST'],
        port=app.config['PORT']
    )

if __name__ == '__main__':
    main()