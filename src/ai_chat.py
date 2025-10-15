#!/usr/bin/env python3
"""
AI対話モジュール
OpenAI ChatGPT APIを使用して対話応答を生成する
"""

import os
import logging
from typing import List, Dict, Optional, Union
from openai import OpenAI


class AIChat:
    """AI対話クラス"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 model: str = "gpt-3.5-turbo",
                 system_prompt: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー。Noneの場合は環境変数OPENAI_API_KEYを使用
            model: 使用するChatGPTモデル
            system_prompt: システムプロンプト（AIの役割や性格を定義）
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYを設定するか、api_key引数を指定してください。")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)
        
        # デフォルトのシステムプロンプト
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
        # 会話履歴
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def _get_default_system_prompt(self) -> str:
        """デフォルトのシステムプロンプトを取得"""
        return """あなたは親しみやすいAIアシスタントです。以下の特徴を持っています：

1. 日本語で自然な会話をします
2. 簡潔で分かりやすい回答を心がけます
3. ユーザーの質問に対して親切で丁寧に答えます
4. 必要に応じて質問を返すことで会話を続けます
5. 音声対話システムなので、短めの文章で回答します

ユーザーとの楽しい会話を楽しみにしています！"""
    
    def chat(self, user_message: str, 
             max_tokens: int = 150,
             temperature: float = 0.7,
             reset_conversation: bool = False) -> str:
        """
        ユーザーメッセージに対してAI応答を生成する
        
        Args:
            user_message: ユーザーのメッセージ
            max_tokens: 最大トークン数
            temperature: 応答の創造性（0.0-1.0）
            reset_conversation: 会話履歴をリセットするかどうか
            
        Returns:
            AIの応答メッセージ
            
        Raises:
            openai.OpenAIError: API呼び出しでエラーが発生した場合
        """
        if reset_conversation:
            self.reset_conversation()
        
        # ユーザーメッセージを履歴に追加
        self.conversation_history.append({
            "role": "user", 
            "content": user_message
        })
        
        self.logger.info(f"ユーザーメッセージ: {user_message}")
        
        try:
            # ChatGPT APIを呼び出し
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # AI応答を履歴に追加
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            self.logger.info(f"AI応答: {ai_response}")
            return ai_response
            
        except Exception as e:
            self.logger.error(f"ChatGPT API エラー: {e}")
            # エラー時はユーザーメッセージを履歴から削除
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()
            raise
    
    def reset_conversation(self):
        """会話履歴をリセットする"""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.logger.info("会話履歴をリセットしました")
    
    def set_system_prompt(self, prompt: str):
        """
        システムプロンプトを変更する
        
        Args:
            prompt: 新しいシステムプロンプト
        """
        self.system_prompt = prompt
        # 会話履歴のシステムメッセージを更新
        if self.conversation_history and self.conversation_history[0]["role"] == "system":
            self.conversation_history[0]["content"] = prompt
        else:
            self.conversation_history.insert(0, {"role": "system", "content": prompt})
        
        self.logger.info("システムプロンプトを更新しました")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        会話履歴を取得する
        
        Returns:
            会話履歴のリスト
        """
        return self.conversation_history.copy()
    
    def save_conversation(self, file_path: str):
        """
        会話履歴をファイルに保存する
        
        Args:
            file_path: 保存先ファイルパス
        """
        import json
        from datetime import datetime
        
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "system_prompt": self.system_prompt,
            "conversation": self.conversation_history
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"会話履歴を保存しました: {file_path}")
    
    def load_conversation(self, file_path: str):
        """
        会話履歴をファイルから読み込む
        
        Args:
            file_path: 読み込み元ファイルパス
        """
        import json
        
        with open(file_path, 'r', encoding='utf-8') as f:
            conversation_data = json.load(f)
        
        self.conversation_history = conversation_data["conversation"]
        self.system_prompt = conversation_data.get("system_prompt", self.system_prompt)
        
        self.logger.info(f"会話履歴を読み込みました: {file_path}")


def main():
    """テスト用のメイン関数"""
    import argparse
    
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='AI対話テスト')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='使用するChatGPTモデル')
    parser.add_argument('--interactive', action='store_true', help='対話モード')
    
    args = parser.parse_args()
    
    try:
        # AIChatインスタンスを作成
        ai_chat = AIChat(model=args.model)
        
        if args.interactive:
            print("=== AI対話システム ===")
            print("メッセージを入力してください。'quit'で終了します。")
            print()
            
            while True:
                user_input = input("あなた: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了']:
                    print("対話を終了します。")
                    break
                
                if not user_input:
                    continue
                
                try:
                    response = ai_chat.chat(user_input)
                    print(f"AI: {response}\n")
                except Exception as e:
                    print(f"エラーが発生しました: {e}\n")
        else:
            # 単発テスト
            test_message = "こんにちは！今日の天気はどうですか？"
            print(f"テストメッセージ: {test_message}")
            
            response = ai_chat.chat(test_message)
            print(f"AI応答: {response}")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
