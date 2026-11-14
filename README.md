# BikeShop

Aplicação de dashboard de estoque em Python/Streamlit, conectada à view
`public.bikeshop_catalog_view` do Supabase.

## Executar localmente

1. Use Python 3.10 ou superior e instale as dependências:

   ```bash
   make install
   ```

2. Crie o arquivo local de credenciais e preencha `SUPABASE_URL` e
   `SUPABASE_KEY`:

   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

   O Streamlit **não lê** o arquivo `.example`; ele lê `secrets.toml` ou as
   variáveis de ambiente. O arquivo `secrets.toml` é ignorado pelo Git.
3. Execute o dashboard:

   ```bash
   make run
   ```

Execute `make help` para ver os comandos disponíveis.

## Estrutura do dashboard

- `src/dashboard/app.py`: inicialização e coordenação do fluxo.
- `src/dashboard/catalog.py`: acesso à view Supabase e agregações do catálogo.
- `src/dashboard/charts.py`: construção dos gráficos com Altair.
- `src/dashboard/ui.py`: coordenação de filtros, cartões, abas e tabela.
- `src/dashboard/views/`: classes de apresentação para estoque, catálogo e preços.
- `src/dashboard/settings.py`: configuração e formatação de valores.

A chave deve ter acesso de leitura à view e às tabelas subjacentes conforme as
políticas RLS do projeto. Os scripts SQL habilitam RLS, mas não criam políticas
de leitura; configure políticas apropriadas para o papel usado pelo dashboard.
Como a aplicação não implementa login, publique-a somente atrás de um controle
de acesso confiável. Guarde a chave apenas em secrets/variáveis de ambiente:
nunca use uma chave `service_role` em uma aplicação pública nem envie
credenciais ao repositório.

O dashboard apresenta cartões de modelos, unidades e valor potencial do
estoque, filtros por marca e categoria e 12 gráficos sobre estoque, catálogo,
preços e margens. Os valores são estimativas do estoque atual; os scripts
existentes não contêm uma tabela de vendas nem dados históricos de receita, por
isso o dashboard não demonstra faturamento, produtos mais vendidos ou evolução
mensal.
