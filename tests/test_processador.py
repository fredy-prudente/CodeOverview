import unittest
import os
from CodeOverview.logic.processador import ProcessadorEstrutura

class TestProcessadorEstrutura(unittest.TestCase):
    def setUp(self):
        self.processador = ProcessadorEstrutura()
        # Crie um diretório de teste com alguns arquivos
        self.test_dir = "test_project"
        os.makedirs(self.test_dir, exist_ok=True)
        # Arquivos de teste
        self.files = {
            "app/utils/utilsllm.py": "def minha_funcao():\n    pass",
            "app/service/jogadorservice.py": "class JogadorService:\n    pass",
            "data/config.json": '{"configuracao": true}',
            "data/styles.css": "body { background-color: #fff; }",
            "index.html": "<!DOCTYPE html><html></html>",
            "main.js": "function main() { console.log('Olá, Mundo!'); }",
            "README.md": "# Teste",
            "script.sh": "echo 'Hello World'"
        }
        for path, content in self.files.items():
            full_path = os.path.join(self.test_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def tearDown(self):
        # Remova o diretório de teste após os testes
        import shutil
        shutil.rmtree(self.test_dir)

    def test_processar_projeto(self):
        extensoes = ['.py', '.json', '.html', '.css', '.js']
        estrutura, erros = self.processador.processar_projeto(self.test_dir, extensoes)
        self.assertIsNotNone(estrutura)
        self.assertEqual(len(erros), 0)
        # Verifique se os arquivos corretos foram incluídos
        for path in self.files:
            ext = os.path.splitext(path)[1]
            if ext.lower() in extensoes:
                self.assertIn(f"{path}:", estrutura)

    def test_processar_projeto_com_erros(self):
        # Adicione um arquivo com conteúdo não decodificável
        arquivo_invalido = os.path.join(self.test_dir, "app", "invalid.py")
        with open(arquivo_invalido, 'wb') as f:
            f.write(b'\xff\xfe\xfd')  # Bytes inválidos para UTF-8

        extensoes = ['.py']
        estrutura, erros = self.processador.processar_projeto(self.test_dir, extensoes)
        self.assertIsNotNone(estrutura)
        self.assertEqual(len(erros), 1)
        self.assertIn("Erro de decodificação: app/invalid.py", erros)

    def test_salvar_estrutura(self):
        extensoes = ['.py']
        estrutura, _ = self.processador.processar_projeto(self.test_dir, extensoes)
        arquivo_saida = "estrutura_teste.txt"
        self.processador.salvar_estrutura(arquivo_saida, estrutura)
        self.assertTrue(os.path.exists(arquivo_saida))
        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        self.assertIn("app/utils/utilsllm.py:", conteudo)
        os.remove(arquivo_saida)

    def test_copiar_para_clipboard(self):
        # Este teste não será efetivamente realizado aqui, mas você pode verificar manualmente.
        extensoes = ['.py']
        estrutura, _ = self.processador.processar_projeto(self.test_dir, extensoes)
        # Chamar a função sem erros
        try:
            self.processador.copiar_para_clipboard(estrutura)
        except Exception as e:
            self.fail(f"Falha ao copiar para o clipboard: {str(e)}")

if __name__ == '__main__':
    unittest.main()
