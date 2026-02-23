### **Contexto**

Você é um desenvolvedor sênior em Flutter/Dart, trabalhando num app com **Clean Architecture**.
O código seguirá as camadas: domain → data → external.
Tratamento de erros com Either (Right/Left).
Stack principal: Flutter 3.x, Dio, dartz.

---

### **Objetivo**

Implementar a feature **"Buscar Endereço por CEP"**, consumindo a API pública do **ViaCEP**.
O use case principal deve receber um CEP e retornar um **AddressEntity** com os campos do endereço.

---

### **Instruções específicas**

* Endpoint da API: `https://viacep.com.br/ws/{CEP}/json/`
* Validar o formato do CEP (aceitar `NNNNNNNN` ou `NNNNN-NNN`).
* Tratar erros de validação, rede e timeout.
* Mapear os campos principais da resposta (`cep`, `logradouro`, `bairro`, `localidade`, `uf`, etc.).
* Aplicar princípios de Clean Architecture: separação clara entre camadas, injeção de dependência e uso de interfaces.
* Garantir testabilidade (mocks ou Fakes nos testes unitários).
* Não usar pacotes externos além de Dio e dartz.

---

### **Formato da resposta**

* Responder de forma estruturada e didática.
* Explicar o raciocínio técnico, camadas envolvidas e responsabilidades de cada uma.
* Incluir breve explicação de como testar a feature.
* Não incluir código, apenas o **plano técnico completo de implementação**.

---

### **Persona / Tom**

Aja como um **desenvolvedor sênior** explicando para um **time de nível intermediário**.
Mantenha o tom técnico, claro e direto, evitando jargões desnecessários.

---

### **Critérios de Aceite**

1. O **use case** deve validar o CEP antes da chamada à API.
2. A resposta da API deve ser convertida corretamente para o modelo de domínio (`AddressEntity`).
3. Casos de erro (`erro-true`, timeout, CEP inexistente) devem retornar uma falha controlada.
4. A implementação deve respeitar a **App Architecture - MVVM (Model-View-ViewModel)** (cada camada com sua responsabilidade).
5. Todos os testes unitários devem passar (use case, repository e model).
6. Nenhuma dependência externa além de **Dio** deve ser utilizada.
7. O código deve estar documentado e com nomes semânticos e consistentes.
8. O tempo de resposta deve respeitar o timeout configurado.
9. O comportamento deve estar alinhado com o padrão de falhas usado no restante do app.