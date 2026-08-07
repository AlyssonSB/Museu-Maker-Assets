import os
import json
import subprocess


def generate_index(base_folder):

    if not os.path.exists(base_folder):
        return

    for year in os.listdir(base_folder):

        year_path = os.path.join(
            base_folder,
            year
        )

        if not os.path.isdir(year_path):
            continue

        items = []

        for item in os.listdir(year_path):

            item_path = os.path.join(
                year_path,
                item
            )

            if not os.path.isdir(item_path):
                continue

            metadata_path = os.path.join(
                item_path,
                "metadata.json"
            )

            if not os.path.exists(metadata_path):
                print(f"Sem metadata: {item_path}")
                continue

            try:

                with open(
                    metadata_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    metadata = json.load(file)

                items.append({
                    "id": metadata.get("id", item),
                    "title": metadata.get(
                        "title",
                        "Sem título"
                    )
                })

            except Exception as error:

                print(
                    f"Erro lendo {metadata_path}: {error}"
                )

        index = {
            "year": int(year),
            "items": items
        }

        output = os.path.join(
            year_path,
            "index.json"
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                index,
                file,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Gerado: {output} ({len(items)} itens)"
        )


def convert_to_webm(base_folder):

    if not os.path.exists(base_folder):
        return

    for root, dirs, files in os.walk(base_folder):

        for filename in files:

            if not filename.lower().endswith(".mp4"):
                continue

            mp4_path = os.path.join(
                root,
                filename
            )

            webm_path = os.path.splitext(
                mp4_path
            )[0] + ".webm"

            # Se o WebM existe e é mais novo que o MP4,
            # não precisamos converter novamente.
            if os.path.exists(webm_path):

                mp4_time = os.path.getmtime(
                    mp4_path
                )

                webm_time = os.path.getmtime(
                    webm_path
                )

                if webm_time >= mp4_time:

                    print(
                        f"WebM atualizado: {webm_path}"
                    )

                    continue

                print(
                    f"MP4 atualizado. "
                    f"Reconvertendo: {mp4_path}"
                )

            else:

                print(
                    f"WebM não existe. "
                    f"Convertendo: {mp4_path}"
                )

            try:

                subprocess.run(
                    [
                        "ffmpeg",

                        "-y",

                        "-i",
                        mp4_path,

                        # Vídeo
                        "-c:v",
                        "libvpx",

                        # Qualidade do vídeo
                        "-crf",
                        "30",

                        # Velocidade/qualidade
                        "-deadline",
                        "good",

                        # Limite de bitrate
                        "-b:v",
                        "2M",

                        # Áudio
                        "-c:a",
                        "libvorbis",

                        "-q:a",
                        "5",

                        webm_path
                    ],
                    check=True
                )

                print(
                    f"WebM criado: {webm_path}"
                )

            except subprocess.CalledProcessError as error:

                print(
                    f"Erro convertendo "
                    f"{mp4_path}: {error}"
                )


convert_to_webm("videos")

generate_index("arts")
generate_index("videos")
