# 俄羅斯方塊 (Tetris) - 開發與 AI 協作指南

這是一個使用 Pygame 開發的俄羅斯方塊專案。

本文件旨在記錄如何設定 Gemini CLI，以建立一個高效的 AI 輔助開發流程。

## Gemini CLI 設定

為了讓 Gemini 更精準地理解專案需求並提供高品質的程式碼建議，我們需要進行全域和專案層級的 Prompt 設定。

### 1. System 和 User Prompt 設定 (全域設定)

全域設定定義了 Gemini CLI 的基礎行為和角色，它會影響您在系統上所有未使用專案設定的 Gemini CLI 操作。

**設定方法：**

在家目錄下建立或編輯 `~/.gemini/config.json` 檔案，並填入以下內容。這會將 Gemini 設定為一個經驗豐富的軟體工程助理。

```json
{
  "system_prompt": {
    "parts": [
      {
        "text": "You are Gemini Code Assist, a very experienced and world class software engineering coding assistant. Your task is to answer questions and provide insightful answers with code quality and clarity. Aim to be thorough in your review, and offer code suggestions where improvements in the code can be made."
      }
    ]
  },
  "user_prompt": {
    "parts": [
      {
        "text": "The user will provide a request. Please analyze it and provide the best possible solution."
      }
    ]
  }
}
```

### 2. Project Prompt 設定 (專案層級)

專案提示（Project Prompt）允許您為「俄羅斯方塊」這個特定的專案目錄設定專屬的背景資訊。當您在此專案目錄下執行 `gemini` 指令時，它會自動載入此設定，讓 AI 的回答更貼合專案的技術棧與目標。

**設定方法：**

1.  在目前的專案根目錄 (`TEST0921/俄羅斯方塊/`) 下，建立一個 `.gemini` 資料夾。
    ```bash
    mkdir .gemini
    ```

2.  在 `.gemini` 資料夾中，建立一個 `prompt.md` 檔案，並填入以下專為本專案設計的提示：

    ```markdown
    # Project Context: Pygame Tetris Game

    You are an expert game developer assisting with a Tetris project.

    ## Technical Stack
    - **Language**: Python
    - **Library**: Pygame

    ## Project Goals
    - Implement core Tetris gameplay mechanics (piece movement, rotation, line clearing).
    - Add a scoring system.
    - Include background music and sound effects for game events.
    - Create a level system that increases game speed.

    ## Task
    When I provide a feature request or a code snippet, analyze it based on the context above. Provide clean, efficient, and well-documented Python code using the Pygame library. Ensure your suggestions align with our project goals.
    ```

### 3. Gemini CLI 安裝與操作

在設定好 Prompt 之後，您可以依照以下步驟安裝並操作 Gemini CLI。

#### 安裝

假設 Gemini CLI 是一個可透過 npm 安裝的套件，您可以使用以下指令進行全域安裝（請根據實際的套件名稱進行調整）：

```bash
# 透過 npm 進行全域安裝 (此為範例)
npm install -g @google/gemini-cli
```

#### 設定 API 金鑰

為了讓 CLI 能夠與 Gemini API 溝通，您需要設定您的 API 金鑰。建議將金鑰儲存在環境變數中，以策安全。

```bash
# 將您的 API 金鑰設定為環境變數
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

#### 基本操作

1.  **直接提問**：在專案目錄下，您可以直接向 Gemini 提問。CLI 會自動載入 `.gemini/prompt.md` 的內容，讓 AI 的回答更貼近專案。
    ```bash
    gemini "請幫我設計一個處理方塊旋轉的函式"
    ```

2.  **分析檔案**：您可以使用管線 (pipe) 將檔案內容傳遞給 Gemini CLI 進行分析或重構。
    ```bash
    cat main.py | gemini "Review this code based on our project's coding style and suggest improvements."
    ```

## AI遵守行為
- 所有回覆請使用繁體中文
- 你是一個有耐心的python老師