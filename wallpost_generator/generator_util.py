import logging
import os
import random

import chevron

log = logging.getLogger(__name__)


def load_file(file_path, name="item"):
    assert file_path, "File path cannot be empty"
    log.info("Start loading %s from: %s", name, file_path)
    with open(file_path, "r") as f:
        text = f.read()
        log.info("Finish loading %s from: %s", name, file_path)
        return text


def files_from_dir(dir_path, name="items"):
    assert dir_path, "Dir path cannot be empty"
    if not dir_path.endswith("/"):
        dir_path = dir_path + "/"
    files = os.listdir(dir_path)
    log.info("Existed %s in %s: %s", name, dir_path, files)
    return list(map(lambda file: dir_path + file, files))


def choose_random(lst, name="item"):
    assert lst, "List cannot be empty"
    item = random.choice(lst)
    log.info("Chosen random %s: %s", name, item)
    return item


def shuffle(lst, name="items"):
    assert lst, "List cannot be empty"
    log.info("Start shuffle %s: %s", name, lst)
    random.shuffle(lst)
    log.info("Shuffle %s result: %s", name, lst)
    return lst


def render_template(template, data):
    log.info("Before render template: %s", template)
    result = chevron.render(template, data)
    log.info("After render template: %s", result)
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
        assert products, "Products cannot be empty"
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
        log.info("Chosen %d random images: %s", count, result)
    return result


if __name__ == '__main__':
    resources_path = "./resources/"
    message = load_and_render(f"{resources_path}templates",
                              f"{resources_path}products.txt",
                              None, None)
