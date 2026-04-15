import os

class LogAnalyzer:
    def __init__(self, fichier: str):
        if not os.path.exists(fichier):
            raise FileNotFoundError(f"File '{fichier}' not found")
        self.fichier = fichier

    def _is_error(self, line: str) -> bool:
        return "[ERROR]" in line

    def extraire_erreurs(self):
        for line in open(self.fichier, "r", encoding="utf-8"):
            if self._is_error(line):
                yield line.strip()

    def sauvegarder_erreurs(self, output: str):
        errors = list(self.extraire_erreurs())
        if not errors:
            print("[INFO] No errors found.")
            return
        with open(output, "w", encoding="utf-8") as f:
            f.write("\n".join(errors))
        print(f"[✔] {len(errors)} error(s) saved to '{output}'")


# --- Run ---
analyzer = LogAnalyzer("server.log")
analyzer.sauvegarder_erreurs("errors_only.txt")
