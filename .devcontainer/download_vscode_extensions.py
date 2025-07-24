import json
import os
import sys
import urllib.request
from urllib.error import HTTPError, URLError


def download_extension(extension_id, output_dir):
    API_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    HEADERS = {"Content-Type": "application/json"}

    # Формируем тело запроса для API
    payload = {
        "filters": [{
            "criteria": [{
                "filterType": 7,
                "value": extension_id
            }],
            "pageNumber": 1,
            "pageSize": 1
        }],
        "flags": 16
    }

    try:
        # Получаем информацию о расширении
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=HEADERS,
            method="POST"
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

            # Извлекаем URL для скачивания
            asset_uri = data["results"][0]["extensions"][0]["versions"][0]["assetUri"]
            vsix_url = f"{asset_uri}/Microsoft.VisualStudio.Services.VSIXPackage"

            # Скачиваем файл
            filename = f"{extension_id.replace('.', '-')}.vsix"
            output_path = os.path.join(output_dir, filename)

            urllib.request.urlretrieve(vsix_url, output_path)
            print(f"Успешно: {filename}")

    except (HTTPError, URLError) as e:
        print(f"Ошибка при скачивании {extension_id}: {str(e)}")
    except KeyError:
        print(f"Неверный формат ответа для {extension_id}")
    except Exception as e:
        print(f"Неизвестная ошибка с {extension_id}: {str(e)}")


def main():
    if len(sys.argv) != 3:
        print("Использование: python script.py <devcontainer.json> <output_dir>")
        sys.exit(1)

    config_file = sys.argv[1]
    output_dir = sys.argv[2]

    # Создаем директорию, если не существует
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Извлекаем список расширений
        extensions = config.get("customizations", {}).get("vscode", {}).get("extensions", [])

        if not extensions:
            print("Расширения не найдены в devcontainer.json")
            return

        print(f"Найдено расширений: {len(extensions)}")

        for ext in extensions:
            if isinstance(ext, str) and len(ext.split(".")) >= 2:
                print(f"Скачиваю: {ext}")
                download_extension(ext, output_dir)
            else:
                print(f"Пропускаю невалидный ID: {ext}")

    except FileNotFoundError:
        print(f"Файл {config_file} не найден")
    except json.JSONDecodeError:
        print("Ошибка парсинга JSON")


if __name__ == "__main__":
    main()
