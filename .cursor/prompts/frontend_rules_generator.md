Atue como um "Project Rule Builder" para o frontend deste repositório React 19 + TypeScript + Vite.

Objetivo: criar/atualizar um conjunto de Project Rules (.mdc) em pt-BR dentro de `.cursor/rules/`, baseadas:

1) no estado REAL do projeto (pastas, dependências, padrões já usados)

2) nas boas práticas oficiais do ecossistema:

- React: https://react.dev/learn
- TypeScript: https://www.typescriptlang.org/docs/handbook/
- Vite: https://vite.dev/guide/
- ESLint: regras configuradas no `package.json` (preset `react-app`)
- Se não conseguir acessar os links, derive as regras a partir do `package.json`, `tsconfig.json`, `vite.config.ts` e do código existente.


## DEVE/NÃO DEVE

- Caso tenha alguma dúvida ou algo que não esteja claro, **VOCÊ DEVE** perguntar ao usuário para esclarecer antes de continuar.
- Caso tenha alguma dúvida ou algo que não esteja claro, **VOCÊ NÃO DEVE** continuar sem esclarecer.


## Contexto do projeto

Este é o frontend de um **chat com IA** (AI Chat). Stack atual:
- **React 19** com `react-dom` (SPA, não SSR/Next.js)
- **TypeScript 5.8** com `strict: true`
- **Vite 6** como bundler (`@vitejs/plugin-react`)
- **@crayonai/react-ui** e **@thesysai/genui-sdk** para componentes de chat com IA
- **lucide-react** para ícones
- **react-markdown** para renderização de Markdown
- **ESLint** configurado inline no `package.json` (extends `react-app`, `react-app/jest`)
- Proxy no Vite para `/api` → `http://127.0.0.1:8000` (backend FastAPI)
- Sem Tailwind CSS, sem state management externo, sem lib de roteamento no momento


### Entrada opcional

- É possível fornecer um arquivo complementar com informações/contexto para orientar a geração das rules.
- Formatos aceitos: `.md`, `.mdc`, `.txt`, `.json`, `.yaml`.
- Tratamento:
  - Leia o arquivo integralmente e extraia diretrizes úteis (decisões arquiteturais, exceções locais, convenções do time, restrições de segurança, etc.).
  - Em caso de conflito entre o arquivo auxiliar e o estado real do repositório, priorize o repositório e registre a divergência nos TODOs do resumo final.
  - Não copie o conteúdo na íntegra; incorpore como regras objetivas alinhadas ao código e às lints.
  - No resumo final, indique o nome do arquivo usado como "Fonte auxiliar".


### O que analisar no repo

- `ui/package.json` (dependências → detectar state management, roteamento, libs de HTTP, UI kits, ícones).
- ESLint configurado inline no `package.json` → campo `"eslintConfig"`.
- `ui/tsconfig.json` / `ui/tsconfig.node.json` (configurações de TypeScript: strict mode, paths, target, etc.).
- `ui/vite.config.ts` (plugins, aliases, proxy, variáveis de ambiente).
- Presença/ausência de Tailwind CSS (atualmente **não há**).
- Estrutura `ui/src/**`, `ui/public/**`.
- Presença de `components/`, `hooks/`, `contexts/`, `services/`, `utils/`, `pages/`, `views/`, `types/`, `lib/`.
- Uso de SDKs de chat/IA: `@crayonai/react-ui`, `@thesysai/genui-sdk`.
- Configuração do proxy no Vite (comunicação com backend).
- Arquivo auxiliar (opcional), quando fornecido (ver "Entrada opcional").


### Saída esperada (arquivos e conteúdo)

Crie/atualize **exatamente** estes arquivos, com front-matter e conteúdo conciso em bullets:


1) `.cursor/rules/frontend-typescript-standards.mdc` (Always)

- `description`: Padrões de código TypeScript/React do projeto frontend.
- Regras: formatter (ESLint com preset react-app), imports (ordem e agrupamento), naming conventions (PascalCase para componentes, camelCase para funções/variáveis, UPPER_SNAKE_CASE para constantes), tipagem estrita (evitar `any`, preferir `unknown`), uso de `const`/`let` (nunca `var`), async/await, template literals, optional chaining, nullish coalescing, logs (sem `console.log` em prod).
- Alinhe às regras do `tsconfig.json` do projeto (`strict: true`, `noUnusedLocals`, `noUnusedParameters`).
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


2) `.cursor/rules/frontend-react-architecture.mdc` (Auto-attach)

- `globs`: `"ui/src/**"`.
- Padrão arquitetural do projeto: SPA com React 19 + Vite; organização por feature/módulo; separação de lógica de negócio dos componentes visuais; direções de dependência (views → hooks/services → types/models).
- Integração com SDKs de chat (`@crayonai/react-ui`, `@thesysai/genui-sdk`).
- Seções: Objetivo, Estrutura por feature/camada, Direções de dependência, Anti-padrões, Checklist.


3) `.cursor/rules/frontend-react-components.mdc` (Auto-attach)

- `globs`: `"ui/src/**/*.tsx"`.
- Regras: componentes funcionais (nunca classes), props tipadas com `interface` ou `type`, destructuring de props, composição sobre herança, custom hooks para lógica reutilizável, memoização (`React.memo`, `useMemo`, `useCallback`) quando necessário, keys em listas, acessibilidade (a11y), lazy loading com `React.lazy`/`Suspense`, uso correto de `"use client"` (apenas se/quando migrar para framework com RSC).
- Padrões específicos do React 19 (use, Actions, useFormStatus, useOptimistic).
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


4) `.cursor/rules/frontend-state-management.mdc` (Auto-attach)

- `globs`: `"ui/src/**"`.
- Estado atual: sem lib de state management externo → usar React state local (`useState`, `useReducer`) e Context API.
- Defina quando usar estado local vs contexto global; imutabilidade; estrutura de estados (loading/error/success); side-effects com `useEffect`; estratégias para evitar re-renders desnecessários.
- Se detectar adoção futura de Zustand, Redux, Jotai, React Query, etc., ajustar as regras.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


5) `.cursor/rules/frontend-project-structure.mdc` (Auto-attach)

- `globs`: `"ui/src/**","ui/public/**"`.
- Árvore de pastas real do projeto; convenções de nomes de arquivos (`*.tsx` para componentes, `*.ts` para lógica pura, `*.css` para estilos); estrutura recomendada (quando o app crescer): `components/`, `hooks/`, `services/`, `types/`, `utils/`, `pages/` ou `views/`; regras de import (relativo vs absoluto com alias); onde criar novos arquivos.
- Seções: Objetivo, Regras, Exemplos curtos, Checklist.


6) `.cursor/rules/frontend-styling.mdc` (Auto-attach)

- `globs`: `"ui/src/**/*.tsx"`, `"ui/src/**/*.css"`.
- Estado atual: CSS puro (sem Tailwind, sem CSS-in-JS, sem CSS Modules detectados); uso de reset CSS via CDN; fonte Inter via Google Fonts.
- Regras: organização de estilos, quando usar classes CSS vs inline styles (evitar inline), responsividade (mobile-first), acessibilidade visual, dark mode (se aplicável).
- Se o projeto adotar Tailwind, CSS Modules ou styled-components no futuro, ajustar.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


7) `.cursor/rules/frontend-services-and-api.mdc` (Auto-attach)

- `globs`: `"ui/src/**"`.
- Comunicação com backend: proxy Vite (`/api` → `http://127.0.0.1:8000`); padrão de HTTP client (fetch, axios, etc.); tipagem de requests/responses; tratamento de erros; streaming (SSE/WebSocket para chat); variáveis de ambiente (`import.meta.env`); nunca expor secrets no client-side.
- Integração com SDKs: `C1Chat` do `@thesysai/genui-sdk` já abstrai a comunicação via `apiUrl`.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


8) `.cursor/rules/frontend-testing.mdc` (Auto-attach)

- `globs`: `"ui/src/**/*.test.ts","ui/src/**/*.test.tsx","ui/src/**/*.spec.ts","ui/src/**/*.spec.tsx","ui/tests/**","ui/__tests__/**"`.
- Estado atual: sem testes configurados (detectar `@testing-library/dom` nas deps); framework sugerido: Vitest (integra com Vite) + Testing Library.
- Tipos: unit/component/integration; quando mockar vs usar fakes; cobertura alvo; fixtures; testes de hooks e componentes.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


9) `.cursor/rules/frontend-vite-config.mdc` (Auto-attach)

- `globs`: `"ui/vite.config.ts"`.
- Configurações do Vite: plugins (`@vitejs/plugin-react`), proxy (regras para proxy de API), aliases de path, variáveis de ambiente, build settings, otimização de deps.
- Seções: Objetivo, Regras, Checklist.


10) `.cursor/rules/commits-and-language.mdc` (Always)

- Commits semânticos em **pt-BR** (feat/fix/chore/docs/refactor/test): título curto + corpo explicando o quê/por quê; referência a issues/PRs; padrão para PRs (título/descrição/labels).
- Seções: Objetivo, Padrões, Exemplos curtos, Checklist.


### Opcionais (criar somente se o repo indicar necessidade)

- `.cursor/rules/frontend-routing.mdc` (Auto-attach se detectar React Router, TanStack Router ou outra lib de roteamento).
- `.cursor/rules/frontend-i18n.mdc` (Auto-attach se houver `i18n/`, `locales/`, ou libs como `react-i18next`/`next-intl`).
- `.cursor/rules/frontend-security.mdc` (Always: `.env`/secrets, `import.meta.env`, no-logs sensíveis, CORS, XSS, sanitização de inputs).
- `.cursor/rules/frontend-performance.mdc` (Auto-attach se necessário: code splitting, lazy loading, bundle analysis, image optimization, Web Vitals).
- `.cursor/rules/frontend-ai-chat-patterns.mdc` (Auto-attach se houver padrões recorrentes de integração com IA: streaming, mensagens, threads, componentes de chat customizados).


### Requisitos de formatação

- Idioma: pt-BR, direto e assertivo.
- Cada arquivo começa com front-matter YAML: `description`, e **ou** `alwaysApply: true` **ou** `globs: [...]` (para Auto-attach).
- Texto em bullets, seções curtas: Objetivo, Regras, Anti-padrões, Checklist (e "Exemplos curtos" quando útil).
- Não copiar documentação inteira; **alinhe e referencie** (ex.: "seguir regra X do ESLint quando aplicável").
- Limite: regras objetivas (evitar longos parágrafos).


### Passos finais

- Liste no final um "Resumo do que foi detectado" (state mgmt, roteamento, HTTP client/SDKs, estilização, padrão arquitetural, pastas).
- Valide os `globs` com base na árvore real do repo e mostre-os no resumo.
- Se algo estiver ambíguo, proponha defaults sensatos e registre TODOs.
- Se um arquivo auxiliar foi utilizado, inclua no resumo: `Fonte auxiliar: <caminho/arquivo>` e destaque quaisquer decisões derivadas dele.
