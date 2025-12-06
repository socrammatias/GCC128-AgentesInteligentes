import autogen

# CONFIGURAÇÃO (GROQ)
config_list = [
    {
        "model": "llama-3.3-70b-versatile",
        "api_key": "", 
        "base_url": "https://api.groq.com/openai/v1"
    }
]

# ---------------------------------------------------------
# DEFINIÇÃO DOS AGENTES "DIRETOS AO PONTO"
# ---------------------------------------------------------

# Agente 1: O Desenvolvedor (Cérebro)
# Instrução: PROIBIDO CONVERSAR. Apenas código.
desenvolvedor = autogen.AssistantAgent(
    name="Dev_Senior_Python",
    llm_config={"config_list": config_list, "temperature": 0.2}, # Temp baixa = mais preciso, menos criativo/falador
    system_message="""
    Você é uma máquina de gerar código Python.
    REGRAS RÍGIDAS:
    1. NÃO se apresente. NÃO explique o que vai fazer. NÃO peça desculpas.
    2. Receba o pedido e responda IMEDIATAMENTE com o bloco de código completo.
    3. O código deve estar dentro de ```python ... ```.
    4. Ao final do código, escreva uma nova linha apenas com a palavra: TERMINATE.
    """
)

# Agente 2: O Gerente (Você/Executor)
# Instrução: Passa o seu pedido para o Dev e aguarda o 'TERMINATE'.
gerente = autogen.UserProxyAgent(
    name="Gerente_Projeto",
    human_input_mode="NEVER", # Não pede input durante a execução, só no início
    max_consecutive_auto_reply=1, # Evita loop de conversa
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "work_dir": "output_code",
        "use_docker": False
    },
    system_message="Você recebe o código e o executa. Se encontrar 'TERMINATE', o trabalho acabou."
)

# ---------------------------------------------------------
# INTERATIVIDADE
# ---------------------------------------------------------

print("\n--- AGENTES PYTHON (MODO DIRETO) ---")
pedido = input("Digite o software que você quer (Ex: 'Snake game em turtle'): ")

print(f"\n>>> Enviando ordem para o Desenvolvedor: '{pedido}'...\n")

# O chat inicia. O Gerente manda a mensagem e o Dev responde com o código.
gerente.initiate_chat(
    desenvolvedor,
    message=f"Escreva o código Python para: {pedido}. Lembre-se: Apenas código + TERMINATE."
)