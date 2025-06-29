from core.base_parser import BaseConfigParser

class YamlConfigParser(BaseConfigParser):
    """
    Concrete config parser that loads all YAML files from a directory into a dictionary.
    """
    def __init__(self):
        self.configs: Dict[str, Any] = {}

    def load(self, config_dir: str, filenames: Optional[List[str]] = None) -> Dict[str, Any]:
        if not os.path.isdir(config_dir):
            raise FileNotFoundError(f"Config directory not found: {config_dir}")

        files_to_parse = filenames if filenames else [f for f in os.listdir(config_dir) if f.endswith((".yaml", ".yml"))]
        for filename in files_to_parse:
            if not filename.endswith((".yaml", ".yml")):
                continue
            file_path = os.path.join(config_dir, filename)
            with open(file_path, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if data:
                        key = os.path.splitext(filename)[0]
                        self.configs[key] = data
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML file {filename}: {e}")
        return self.configs

    def get(self, key: str, default: Any = None) -> Any:
        return self.configs.get(key, default)