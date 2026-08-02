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

            if os.path.isdir(item_path):

                items.append({
                    "id": item
                })


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
            f"Gerado: {output}"
        )



generate_index("arts")
generate_index("videos")
