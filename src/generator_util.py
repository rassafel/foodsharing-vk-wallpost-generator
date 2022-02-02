import os
import random

import chevron


def load_file(file_path, name="item"):
    assert file_path, "File path cannot be empty."
    print(f"Start loading {name} from:", file_path)
    with open(file_path, "r") as f:
        text = f.read()
        print(f"Finish loading {name} from:", file_path)
        return text


def files_from_dir(dir_path, name="items"):
    assert dir_path, "Dir path cannot be empty."
    if not dir_path.endswith("/"):
        dir_path = dir_path + "/"
    files = os.listdir(dir_path)
    print(f"Existed {name} in {dir_path}:", files)
    return list(map(lambda file: dir_path + file, files))


def choose_random(lst, name="item"):
    assert lst, "List cannot be empty"
    item = random.choice(lst)
    print(f"Chosen random {name}:", item)
    return item


def shuffle(lst, name="items"):
    assert lst, "List cannot be empty"
    print(f"Start shuffle {name}:", lst)
    random.shuffle(lst)
    print(f"Shuffle {name} result:", lst)
    return lst


def render_template(template, data):
    print("Before render template:", template)
    result = chevron.render(template, data)
    print("After render template:", result)
    return result


def load_and_render(templates_path,
                    products_path,
                    names_path,
                    places_path):
    def load_values(products_p,
                    names_p,
                    places_p):
        values = {}

        products = load_file(products_p, "products")
        assert products, "Products cannot be empty."
        products = products.split("\n")
        values["products"] = shuffle(products, "products")
        values["fname"] = "Ivan"
        values["lname"] = "Ivanov"
        return values

    def load_template(templates_p):
        templates = files_from_dir(templates_p, "templates")
        template_path = choose_random(templates, "template")
        return load_file(template_path, "template")

    data = load_values(products_path, names_path, places_path)
    template = load_template(templates_path)
    return render_template(template, data)


def get_photos(images_path, min_count, max_count):
    assert min_count >= 0, "Min cannot be lesser then 0"
    assert min_count < max_count, "Max cannot be lesser then min"

    images = files_from_dir(images_path, "images")
    result = None
    if images:
        shuffle(images, "images")
        count = random.randint(min_count, min(len(images), max_count))
        result = images[:count]
        print(f"Chosen {count} random images:", result)
    return result


if __name__ == '__main__':
    resources_path = "./resources/"
    message = load_and_render(f"{resources_path}templates",
                              f"{resources_path}products.txt",
                              None, None)
