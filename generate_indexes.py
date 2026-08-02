import os
import json


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
                print(
                    f"Sem metadata: {item_path}"
                )
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
                    "title": metadata.get("title", "Sem título")
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



generate_index("arts")
generate_index("videos")
