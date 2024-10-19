@echo off

REM スクリプトの実行場所を取得
set "CURRENT_DIR=%~dp0"

REM 仮想環境のアクティベート
call "%CURRENT_DIR%\..\..\s2svenv\Scripts\activate.bat"

REM ディストリビューションフォルダの作成（存在しない場合のみ）
if not exist "%CURRENT_DIR%\dist" (
    mkdir "%CURRENT_DIR%\dist"
)

REM .streamlitフォルダ以下をdistフォルダにコピー
xcopy /s /e "%CURRENT_DIR%\.streamlit" "%CURRENT_DIR%\dist\.streamlit" /i /y

REM s2s-app.pyをdistフォルダにコピー
copy "%CURRENT_DIR%\s2s-app.py" "%CURRENT_DIR%\dist\s2s-app.py" /y

REM llm_character.tomlをdistフォルダにコピー
copy "%CURRENT_DIR%\llm_character.toml" "%CURRENT_DIR%\dist\llm_character.toml" /y

REM src/util/logger/log/loggingUtil.logをdistフォルダにコピー
if not exist "%CURRENT_DIR%\dist\util\logger\log" (
    mkdir "%CURRENT_DIR%\dist\util\logger\log"
)
copy "%CURRENT_DIR%\src\util\logger\log\loggingUtil.log" "%CURRENT_DIR%\dist\util\logger\log\loggingUtil.log" /y

REM pyinstallerコマンドを実行
pyinstaller run_main.spec --clean

pause

