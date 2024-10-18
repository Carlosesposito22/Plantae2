# 🖥️ SR1

*** 📑 Links importantes:***
<ul>
    <a  href="https://www.figma.com/proto/9YfudFBdVCbdnRiEKH5Hyq/Planta%C3%AA---Projetos-2-%F0%9F%8C%B1?node-id=103-339&node-type=canvas&t=08kK10QCC2D3SZ5t-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=103%3A339"
      >Protótipo de Lo-Fi no Figma</a>
  </li>
   <li>
    <a href="https://drive.google.com/file/d/16oCJANJX6McgLvQhzH-JkIA9ypisI2YP/view?usp=sharing"
      >Screencast - Figma</a>
  </li>
  <li>
    <a href="https://drive.google.com/file/d/1frHRKDRtSO41zwEVjYxHUoN2YnmuS-AE/view?usp=sharing"
      >Screencast - Azure</a>
  </li>
</ul>
<br/>

*** 🕹️ Deployment das histórias:***
<ul>
  <li>
    <a href="https://plantae.azurewebsites.net/accounts/signin/?next=/"
      >Deployment na Azure</a>
  </li>
</ul>
<br/>

*** 📠 Histórias do usuário:***
<br/>
****1. Consultar o Clima Local****
	
Como um pequeno produtor rural,
Eu quero ver as condições climáticas da minha região,
Para que eu possa planejar adequadamente o meu plantio.
Cenário: 
-O produtor acessa a plataforma e a mesma já traz a previsão semanal automaticamente para a região,
-Dado que a aplicação inicialmente será apenas para a região de Carpina-PE,
-Quando ele acessar a página principal,
-Então ele verá as condições climáticas atuais e previsões dos próximos 7 dias.



****2. Programar o Plantio****

Como um pequeno produtor rural,
Eu quero programar as datas de plantio com base nas previsões climáticas,
Para que eu possa garantir que o clima favoreça o desenvolvimento das minhas culturas.
Cenário: 
-O produtor define a cultura e a data de plantio.
-Dado que o produtor selecionou a cultura e a data de plantio desejada,
-Quando ele confirmar a programação,
-Então ele receberá um calendário com marcos importantes de crescimento, bem como sugestões.


****3. Receber Alertas de Clima Crítico****

Como um pequeno agricultor,
Eu quero receber alertas de clima extremos da minha região,
Para que eu possa tomar medidas preventivas e proteger minha produção.
Cenário: 
-O sistema detecta uma previsão de geada, seca, chuvas e ventos fortes.
-Dado que há uma previsão de clima extremo,
-Quando o alerta for emitido,
-Então o produtor receberá uma notificação na página principal da plataforma indicando o alerta.



****4. Gerenciar a Rotação de Culturas****

Como um produtor que pratica agricultura de subsistência,
Eu quero gerenciar a rotação de culturas,
Para que eu mantenha a fertilidade do solo e aumente a produtividade.
Cenário: 
-O produtor define as culturas plantadas e a sequência de rotação.
-Dado que o produtor escolheu as culturas e as datas de colheita,
-Quando a rotação for configurada,
-Então ele receberá lembretes para trocar as culturas de acordo com o plano.

****5. Acompanhar o Calendário de Colheita****

Como um agricultor de subsistência,
Eu quero acompanhar o calendário de colheita,
Para que eu colha os produtos no momento certo.
Cenário: 
-O produtor consulta a plataforma sobre a data prevista para a colheita.
-Dado que o calendário foi programado,
-Quando ele acessar a seção de colheitas,
-Então verá um cronograma detalhado das datas previstas de cada cultura.

****6. Receber Dicas de Boas Práticas Agrícolas****

Como um pequeno produtor,
Eu quero receber dicas sobre plantio e cultivo,
Para que eu possa melhorar a qualidade da minha produção.
Cenário: 
-O produtor acessa a plataforma regularmente.
-Dado que ele planta uma cultura específica,
-Quando acessar a seção de dicas/ dúvidas,
-Então ele verá sugestões personalizadas com base no tipo de cultivo.

****7. Sugestões Personalizadas de Culturas****

Como um agricultor com diferentes opções de cultivo,
Eu quero receber sugestões personalizadas de culturas para plantar,
Para que eu possa escolher as que melhor se adaptam às minhas condições e necessidades.
Cenário: 
-O produtor fornece informações sobre o solo e clima.
-Dado que ele forneceu dados sobre seu solo e clima,
-Quando ele acessar a seção de sugestões,
-Então ele verá recomendações de culturas ideais com base nas condições fornecidas.

****8. Registrar o Histórico de Plantios e Colheitas****

Como um pequeno agricultor,
Eu quero registrar o histórico de plantios e colheitas,
Para que eu possa acompanhar o desempenho de cada safra.
Cenário: 
-O produtor preenche os dados de cada plantio e colheita.
-Dado que ele registrou essas informações,
-Quando acessar o histórico,
-Então verá relatórios sobre o desempenho de cada cultura.

****9. Ajustar Plano de Plantio com Base em Previsões****

Como um agricultor que usa previsões climáticas,
Eu quero ajustar o meu plano de plantio baseado nas novas previsões de tempo,
Para que eu possa minimizar os impactos negativos do clima.
Cenário: 
-O produtor já programou o plantio e há mudanças no clima.
-Dado que a previsão climática mudou,
-Quando ele acessar a programação,
-Então verá recomendações para ajustar a data de plantio.

****10. Monitorar Pragas e Doenças****

Como um pequeno agricultor,
Eu quero receber alertas sobre possíveis pragas e doenças que podem afetar minhas plantações,
Para que eu possa tomar medidas preventivas e proteger minha colheita.
Cenário: 
-O sistema utiliza dados climáticos e históricos de pragas na região.
-Dado que o clima ou o histórico da área indica risco de pragas,
-Quando o alerta for acionado,
-Então o produtor receberá informações sobre a praga ou doença e como preveni-la.

****11. Diagnóstico de Problemas de Cultivo****

Como um agricultor que enfrenta problemas nas plantações,
Eu quero receber diagnósticos e soluções para problemas comuns de cultivo,
Para que eu possa resolver questões rapidamente e manter minhas plantas saudáveis.
Cenário: 
-O produtor descreve os sintomas observados nas plantas.
-Dado  que ele descreveu os problemas,
-Quando ele acessar a seção de diagnóstico,
-Então verá sugestões de problemas possíveis e soluções apropriadas.

****12. Checklist das Tarefas Diárias das Culturas****

Como um pequeno produtor rural,
Eu quero ter acesso a uma checklist diária com todas as tarefas essenciais para o cuidado das minhas culturas,
Para que eu possa garantir que cada etapa, como poda, irrigação e exposição ao sol, seja realizada de forma adequada e no tempo certo.
Cenário: 
-O produtor acessa a plataforma e encontra uma checklist personalizada para cada cultura, com as tarefas diárias organizadas e detalhadas.
-Dado  o produtor selecionou a cultura que está cultivando,
-Quando ele acessar a checklist,
-Então verá uma lista de tarefas essenciais, como horários de poda, quantidade ideal de sol, frequência de irrigação, e cuidados com pragas, para garantir o manejo correto de suas culturas diariamente.


*** ✅ Histórias Implementadas:***

- Consultar o Clima Local
- Receber Alertas de Clima Crítico


*** 📊 Diagrama de atividades:***

 <li>
    <a href="https://excalidraw.com/#room=5ebfd22a9450b3a406b2,kPiWp7b0bE8V-hPd0gU96A"
      >Diagrama de Atividades</a>
  </li>

<br/>

*** 📲 Issues/bug tracker:***
<li>
    <a href="https://drive.google.com/file/d/1_ZvPMthFRryos5dokXCLAoPOi00WcPj9/view?usp=sharing"
      >Bug Trackers</a>
  </li>
<br/>
 