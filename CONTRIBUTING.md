# Guia de Contribuição

Muito obrigado por considerar contribuir com o AutoCommit! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Índice

- [Como Posso Contribuir?](#como-posso-contribuir)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Mensagens de Commit](#mensagens-de-commit)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Melhorias](#sugerindo-melhorias)


## 🤝 Como Posso Contribuir?

Existem várias maneiras de contribuir com o AutoCommit:

- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Submeter correções de bugs
- Implementar novas funcionalidades
- Revisar pull requests

## 🔧 Processo de Desenvolvimento

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork localmente
git clone https://github.com/seu-usuario/autocommit.git
cd autocommit
```

### 2. Crie uma Branch

```bash
# Crie uma branch para sua feature ou correção
git checkout -b nome-da-feature
# ou
git checkout -b descricao-do-bug
```

### 3. Faça suas Alterações

- Escreva código de preferência claro e legível
- Mantenha a documentação atualizada

### 4. Teste suas Alterações

### 5. Commit suas Alterações

```bash
# Adicione os arquivos modificados
git add .

# Faça o commit seguindo as convenções
git commit -m "tipo: descrição breve das alterações"

# Ou até mesmo usar o próprio autocommit pra isso!
autocommit .
```

### 6. Push e Pull Request

```bash
# Envie suas alterações
git push origin feature/nome-da-feature

# Abra um Pull Request no GitHub
```

## 💻 Padrões de Código

### Estilo de Código

- Use identação consistente
- Comente código complexo quando necessário

## 📝 Mensagens de Commit

Usamos commits semânticos. Siga este formato:

```
tipo(escopo): descrição breve

[corpo opcional]

[rodapé opcional]
```

### Tipos de Commit

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Alterações na documentação
- **style**: Formatação, ponto e vírgula, etc
- **refactor**: Refatoração de código
- **test**: Adição ou correção de testes
- **chore**: Tarefas de manutenção

### Exemplos

```bash
feat: adiciona funcionalidade de commit automático

fix: corrige erro ao processar arquivos grandes

docs: atualiza instruções de instalação no README

refactor: reorganiza estrutura de pastas do projeto
```

## 🐛 Reportando Bugs

Ao reportar bugs, inclua:

### Informações Essenciais

- **Descrição clara** do problema
- **Passos para reproduzir** o bug
- **Comportamento esperado** vs **comportamento atual**
- **Sistema operacional** e versão
- **Logs de erro** relevantes

### Template de Issue

```markdown
**Descrição do Bug**
Uma descrição clara e concisa do bug.

**Passos para Reproduzir**
1. Vá para '...'
2. Execute '...'
3. Veja o erro

**Comportamento Esperado**
O que você esperava que acontecesse.

**Ambiente**
- SO: [ex: Windows 10, Ubuntu 22.04]
```

## ✅ Checklist de Pull Request

Antes de submeter um PR, verifique:

- [ ] Todos os testes passam
- [ ] Não há conflitos com a branch principal (opcional)
- [ ] A descrição do PR é clara e completa

## 📞 Dúvidas?

Se tiver dúvidas sobre como contribuir:

- Abra uma issue com uma tag de dúvida como `question`
- Entre em contato através das issues do GitHub
- Consulte a documentação do projeto

---

Obrigadíssimo por ver como contribuir no AutoCommit!
