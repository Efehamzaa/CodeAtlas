import json

class PackageJsonParser:
    def __init__(self):
        pass
    def parse(self , file_content:str) -> list:
        parsed_data=[]

        try:
            data=json.loads(file_content)
        except json.JSONDecodeError:
            return parsed_data

        dependencies = data.get("dependencies" , {})
        dev_dependencies = data.get("devDependencies" , {})

        for isim , versiyon in dependencies.items():
            dict_package={"name":isim , "version":versiyon}
            parsed_data.append(dict_package)

        for isim , versiyon in dev_dependencies.items():
            dict_package_dev={"name":isim , "version":versiyon}
            parsed_data.append(dict_package_dev)

        return parsed_data
