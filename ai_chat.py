#!/usr/bin/env python3
"""
AI対話システム
OpenAI ChatGPT APIを使用した対話機能
"""

import os
import logging
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class AIChat:
    """AI対話クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = self._setup_logging()
        
        # OpenAI API設定
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # 対話設定
        self.model = os.getenv('CHAT_MODEL', 'gpt-4o-mini')
        self.system_prompt = os.getenv('SYSTEM_PROMPT', 'あなたは親切で役立つアシスタントです。日本語で回答してください。')
        
        # 会話履歴
        self.conversation_history: List[Dict[str, str]] = []
        
        self.logger.info("AI対話システムを初期化しました")
    
    def _setup_logging(self):
        """ログ設定"""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def chat(self, user_message: str) -> str:
        """
        ユーザーメッセージに対してAI応答を生成
        
        Args:
            user_message: ユーザーのメッセージ
            
        Returns:
            AI応答のテキスト
        """
        self.logger.info(f"ユーザーメッセージ: {user_message}")
        
        try:
            # 会話履歴にユーザーメッセージを追加
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # システムプロンプトを含むメッセージリストを作成
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            
            # OpenAI APIで応答を生成
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            # AI応答を取得
            ai_response = response.choices[0].message.content.strip()
            
            # 会話履歴にAI応答を追加
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            self.logger.info(f"AI応答: {ai_response}")
            return ai_response
            
        except Exception as e:
            self.logger.error(f"AI対話エラー: {e}")
            return f"申し訳ありません。エラーが発生しました: {str(e)}"
    
    def reset_conversation(self):
        """会話履歴をリセット"""
        self.conversation_history = []
        self.logger.info("会話履歴をリセットしました")
    
    def set_system_prompt(self, prompt: str):
        """
        システムプロンプトを変更
        
        Args:
            prompt: 新しいシステムプロンプト
        """
        self.system_prompt = prompt
        self.logger.info(f"システムプロンプトを変更しました: {prompt}")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        会話履歴を取得
        
        Returns:
            会話履歴のリスト
        """
        return self.conversation_history.copy()
    
    def save_conversation(self, file_path: str):
        """
        会話履歴をファイルに保存
        
        Args:
            file_path: 保存先ファイルパス
        """
        try:
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            self.logger.info(f"会話履歴を保存しました: {file_path}")
        except Exception as e:
            self.logger.error(f"会話履歴の保存に失敗: {e}")
    
    def load_conversation(self, file_path: str):
        """
        会話履歴をファイルから読み込み
        
        Args:
            file_path: 読み込み元ファイルパス
        """
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            self.logger.info(f"会話履歴を読み込みました: {file_path}")
        except Exception as e:
            self.logger.error(f"会話履歴の読み込みに失敗: {e}")


def main():
    """テスト用のメイン関数"""
    print("🤖 AI対話システムテスト")
    print("=" * 50)
    
    try:
        # AI対話システムを初期化
        ai_chat = AIChat()
        
        print("🎯 AI対話を開始します")
        print("💡 メッセージを入力してください")
        print("⏹️  'quit' で終了")
        
        while True:
            try:
                # ユーザー入力
                user_input = input("\n👤 あなた: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了']:
                    print("👋 対話を終了します")
                    break
                
                if not user_input:
                    continue
                
                # AI応答を生成
                print("🤖 AI: 考え中...")
                response = ai_chat.chat(user_input)
                print(f"🤖 AI: {response}")
                
            except KeyboardInterrupt:
                print("\n🛑 終了します...")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                continue
        
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
