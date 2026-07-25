from __future__ import annotations

from dataclasses import dataclass
from difflib import get_close_matches
from typing import Dict, List, Optional

import streamlit as st


@dataclass(frozen=True)
class ESGTerm:
    category: str
    names: Dict[str, str]
    definitions: Dict[str, str]
    aliases: List[str]


LANGUAGES = {
    "한국어": "ko",
    "Español": "es",
    "Русский": "ru",
}

UI_TEXT = {
    "ko": {
        "title": "🌱 다국어 ESG 경영 설명 챗봇",
        "subtitle": "ESG 핵심 용어를 한국어·스페인어·러시아어로 쉽게 설명합니다.",
        "language": "답변 언어",
        "examples": "질문 예시",
        "input": "ESG 용어나 질문을 입력하세요. 예: 탄소중립이 뭐야?",
        "welcome": "안녕하세요! 궁금한 ESG 용어를 입력해 주세요.",
        "category": "분류",
        "term": "용어",
        "definition": "정의",
        "not_found": "해당 용어를 찾지 못했습니다.",
        "suggestion": "다음 용어 중 하나를 질문해 보세요:",
        "supported": "지원 용어",
        "reset": "대화 초기화",
        "disclaimer": "이 챗봇은 학습용 기초형 챗봇이며, 기업 투자 판단이나 전문 자문을 제공하지 않습니다.",
    },
    "es": {
        "title": "🌱 Chatbot multilingüe de ESG",
        "subtitle": "Explica conceptos clave de ESG en coreano, español y ruso.",
        "language": "Idioma de respuesta",
        "examples": "Ejemplos de preguntas",
        "input": "Escribe un término o una pregunta sobre ESG. Ej.: ¿Qué es la neutralidad de carbono?",
        "welcome": "¡Hola! Escribe el término ESG que quieras conocer.",
        "category": "Categoría",
        "term": "Término",
        "definition": "Definición",
        "not_found": "No pude encontrar ese término.",
        "suggestion": "Prueba con uno de estos términos:",
        "supported": "Términos disponibles",
        "reset": "Reiniciar conversación",
        "disclaimer": "Este chatbot es una herramienta educativa básica y no ofrece asesoramiento profesional ni de inversión.",
    },
    "ru": {
        "title": "🌱 Многоязычный чат-бот по ESG",
        "subtitle": "Просто объясняет ключевые понятия ESG на корейском, испанском и русском языках.",
        "language": "Язык ответа",
        "examples": "Примеры вопросов",
        "input": "Введите термин или вопрос об ESG. Например: Что такое углеродная нейтральность?",
        "welcome": "Здравствуйте! Введите интересующий вас термин ESG.",
        "category": "Категория",
        "term": "Термин",
        "definition": "Определение",
        "not_found": "Не удалось найти этот термин.",
        "suggestion": "Попробуйте спросить об одном из следующих терминов:",
        "supported": "Доступные термины",
        "reset": "Очистить диалог",
        "disclaimer": "Этот чат-бот создан для обучения и не предоставляет профессиональных или инвестиционных рекомендаций.",
    },
}

CATEGORY_NAMES = {
    "E": {"ko": "환경(Environment)", "es": "Medioambiente (Environment)", "ru": "Экология (Environment)"},
    "S": {"ko": "사회(Social)", "es": "Sociedad (Social)", "ru": "Социальная сфера (Social)"},
    "G": {"ko": "지배구조(Governance)", "es": "Gobernanza (Governance)", "ru": "Корпоративное управление (Governance)"},
    "ESG": {"ko": "ESG 종합", "es": "ESG general", "ru": "Общее понятие ESG"},
}

TERMS: Dict[str, ESGTerm] = {
    "esg": ESGTerm(
        category="ESG",
        names={"ko": "ESG 경영", "es": "gestión ESG", "ru": "ESG-управление"},
        definitions={
            "ko": "기업이 재무적 성과뿐 아니라 환경 보호, 사회적 책임, 투명한 지배구조를 함께 고려하여 지속가능한 성장을 추구하는 경영 방식입니다.",
            "es": "Es una forma de gestión empresarial que, además de los resultados financieros, considera el medioambiente, la responsabilidad social y una gobernanza transparente para lograr un crecimiento sostenible.",
            "ru": "Это подход к управлению компанией, который наряду с финансовыми результатами учитывает экологию, социальную ответственность и прозрачное корпоративное управление ради устойчивого развития.",
        },
        aliases=["esg", "esg 경영", "환경 사회 지배구조", "gestión esg", "que es esg", "что такое esg", "esg управление"],
    ),
    "carbon_neutrality": ESGTerm(
        category="E",
        names={"ko": "탄소중립", "es": "neutralidad de carbono", "ru": "углеродная нейтральность"},
        definitions={
            "ko": "배출한 온실가스를 최대한 줄이고, 남은 배출량만큼 흡수하거나 제거하여 실질적인 순배출량을 0에 가깝게 만드는 상태입니다.",
            "es": "Es el estado en el que se reducen al máximo las emisiones de gases de efecto invernadero y se compensan o eliminan las restantes para acercar las emisiones netas a cero.",
            "ru": "Это состояние, при котором выбросы парниковых газов максимально сокращаются, а оставшиеся выбросы компенсируются или удаляются, чтобы чистые выбросы приблизились к нулю.",
        },
        aliases=["탄소중립", "탄소 중립", "carbon neutrality", "neutralidad de carbono", "carbono neutro", "углеродная нейтральность", "углеродно нейтральный"],
    ),
    "renewable_energy": ESGTerm(
        category="E",
        names={"ko": "재생에너지", "es": "energía renovable", "ru": "возобновляемая энергия"},
        definitions={
            "ko": "태양광, 풍력, 수력처럼 자연적으로 다시 생성되어 반복해서 사용할 수 있는 에너지입니다.",
            "es": "Es la energía obtenida de fuentes que se regeneran de forma natural, como el sol, el viento y el agua.",
            "ru": "Это энергия из источников, которые естественным образом восстанавливаются, например солнца, ветра и воды.",
        },
        aliases=["재생에너지", "재생 에너지", "renewable energy", "energía renovable", "energia renovable", "возобновляемая энергия", "возобновляемые источники энергии"],
    ),
    "greenhouse_gas": ESGTerm(
        category="E",
        names={"ko": "온실가스", "es": "gases de efecto invernadero", "ru": "парниковые газы"},
        definitions={
            "ko": "대기 중에서 열을 가두어 지구의 온도를 높이는 기체로, 이산화탄소와 메탄 등이 대표적입니다.",
            "es": "Son gases que retienen calor en la atmósfera y elevan la temperatura del planeta, como el dióxido de carbono y el metano.",
            "ru": "Это газы, которые удерживают тепло в атмосфере и повышают температуру Земли, например углекислый газ и метан.",
        },
        aliases=["온실가스", "온실 가스", "greenhouse gas", "gases de efecto invernadero", "gas de efecto invernadero", "парниковые газы", "парниковый газ"],
    ),
    "circular_economy": ESGTerm(
        category="E",
        names={"ko": "순환경제", "es": "economía circular", "ru": "циркулярная экономика"},
        definitions={
            "ko": "제품과 자원을 버리지 않고 재사용·수리·재활용하여 폐기물과 자원 소비를 줄이는 경제 방식입니다.",
            "es": "Es un modelo económico que reduce residuos y consumo de recursos mediante la reutilización, reparación y reciclaje de productos y materiales.",
            "ru": "Это экономическая модель, которая сокращает отходы и потребление ресурсов благодаря повторному использованию, ремонту и переработке продукции и материалов.",
        },
        aliases=["순환경제", "순환 경제", "circular economy", "economía circular", "economia circular", "циркулярная экономика", "экономика замкнутого цикла"],
    ),
    "social_responsibility": ESGTerm(
        category="S",
        names={"ko": "기업의 사회적 책임", "es": "responsabilidad social empresarial", "ru": "корпоративная социальная ответственность"},
        definitions={
            "ko": "기업이 이윤 추구뿐 아니라 노동자, 소비자, 지역사회와 환경에 미치는 영향을 책임 있게 관리하는 것을 의미합니다.",
            "es": "Significa que una empresa gestiona responsablemente su impacto en trabajadores, consumidores, comunidades y medioambiente, además de buscar beneficios.",
            "ru": "Это ответственность компании за влияние на работников, потребителей, местные сообщества и окружающую среду наряду с получением прибыли.",
        },
        aliases=["사회적 책임", "기업의 사회적 책임", "csr", "responsabilidad social", "responsabilidad social empresarial", "социальная ответственность", "корпоративная социальная ответственность", "ксo"],
    ),
    "labor_rights": ESGTerm(
        category="S",
        names={"ko": "노동권", "es": "derechos laborales", "ru": "трудовые права"},
        definitions={
            "ko": "노동자가 안전한 환경에서 정당한 임금과 휴식, 차별받지 않을 권리 등을 보장받는 것을 의미합니다.",
            "es": "Son los derechos de los trabajadores a un entorno seguro, un salario justo, descanso y protección frente a la discriminación, entre otros.",
            "ru": "Это права работников на безопасные условия труда, справедливую оплату, отдых и защиту от дискриминации.",
        },
        aliases=["노동권", "노동자 권리", "labor rights", "derechos laborales", "derechos de los trabajadores", "трудовые права", "права работников"],
    ),
    "supply_chain": ESGTerm(
        category="S",
        names={"ko": "공급망 관리", "es": "gestión de la cadena de suministro", "ru": "управление цепочкой поставок"},
        definitions={
            "ko": "원료 조달부터 생산·운송·판매까지 이어지는 과정에서 환경오염, 인권 침해, 안전 문제 등이 발생하지 않도록 관리하는 활동입니다.",
            "es": "Es la gestión de todo el proceso, desde las materias primas hasta la producción, transporte y venta, para prevenir daños ambientales, vulneraciones de derechos humanos y problemas de seguridad.",
            "ru": "Это управление процессом от закупки сырья до производства, перевозки и продажи с целью предотвращения экологического ущерба, нарушений прав человека и проблем безопасности.",
        },
        aliases=["공급망", "공급망 관리", "supply chain", "cadena de suministro", "gestión de la cadena de suministro", "цепочка поставок", "управление цепочкой поставок"],
    ),
    "industrial_safety": ESGTerm(
        category="S",
        names={"ko": "산업 안전", "es": "seguridad laboral", "ru": "промышленная безопасность"},
        definitions={
            "ko": "작업장에서 사고와 질병을 예방하기 위해 시설, 절차, 교육과 보호 장비 등을 체계적으로 관리하는 것입니다.",
            "es": "Es la gestión sistemática de instalaciones, procedimientos, formación y equipos de protección para prevenir accidentes y enfermedades laborales.",
            "ru": "Это системное управление оборудованием, процедурами, обучением и средствами защиты для предотвращения несчастных случаев и профессиональных заболеваний.",
        },
        aliases=["산업 안전", "산업안전", "workplace safety", "seguridad laboral", "seguridad industrial", "промышленная безопасность", "охрана труда"],
    ),
    "diversity_inclusion": ESGTerm(
        category="S",
        names={"ko": "다양성과 포용성", "es": "diversidad e inclusión", "ru": "разнообразие и инклюзивность"},
        definitions={
            "ko": "성별, 국적, 나이, 장애 등 서로 다른 배경을 존중하고 모든 구성원이 공정하게 참여할 수 있도록 하는 원칙입니다.",
            "es": "Es el principio de respetar diferentes orígenes, como género, nacionalidad, edad o discapacidad, y garantizar una participación justa para todas las personas.",
            "ru": "Это принцип уважения различий, включая пол, национальность, возраст и инвалидность, и обеспечения справедливого участия для всех.",
        },
        aliases=["다양성과 포용성", "다양성", "포용성", "diversity and inclusion", "diversidad e inclusión", "diversidad inclusion", "разнообразие и инклюзивность", "инклюзивность"],
    ),
    "corporate_governance": ESGTerm(
        category="G",
        names={"ko": "기업 지배구조", "es": "gobierno corporativo", "ru": "корпоративное управление"},
        definitions={
            "ko": "기업의 중요한 의사결정을 누가, 어떤 절차와 기준으로 내리고 감독하는지를 정한 체계입니다.",
            "es": "Es el sistema que define quién toma y supervisa las decisiones importantes de una empresa y mediante qué procedimientos y criterios.",
            "ru": "Это система, определяющая, кто и по каким процедурам принимает и контролирует важные решения компании.",
        },
        aliases=["기업 지배구조", "지배구조", "corporate governance", "gobierno corporativo", "корпоративное управление", "корпоративное руководство"],
    ),
    "business_ethics": ESGTerm(
        category="G",
        names={"ko": "윤리경영", "es": "ética empresarial", "ru": "деловая этика"},
        definitions={
            "ko": "기업이 법을 지키는 것을 넘어 정직, 공정성, 책임의 원칙에 따라 의사결정하고 행동하는 경영 방식입니다.",
            "es": "Es una forma de gestión en la que la empresa actúa y toma decisiones con honestidad, equidad y responsabilidad, más allá del mero cumplimiento legal.",
            "ru": "Это подход, при котором компания принимает решения и действует честно, справедливо и ответственно, не ограничиваясь формальным соблюдением закона.",
        },
        aliases=["윤리경영", "기업 윤리", "business ethics", "ética empresarial", "etica empresarial", "деловая этика", "этика бизнеса"],
    ),
    "transparency": ESGTerm(
        category="G",
        names={"ko": "경영 투명성", "es": "transparencia empresarial", "ru": "прозрачность управления"},
        definitions={
            "ko": "기업이 재무 상태, 의사결정, 위험과 성과 등의 정보를 이해관계자에게 정확하고 공개적으로 제공하는 것을 의미합니다.",
            "es": "Significa que una empresa comunica de forma clara y fiable información sobre sus finanzas, decisiones, riesgos y resultados a las partes interesadas.",
            "ru": "Это открытое и достоверное раскрытие заинтересованным сторонам информации о финансах, решениях, рисках и результатах компании.",
        },
        aliases=["경영 투명성", "투명성", "transparency", "transparencia empresarial", "transparencia", "прозрачность управления", "прозрачность"],
    ),
    "stakeholder": ESGTerm(
        category="G",
        names={"ko": "이해관계자", "es": "grupos de interés", "ru": "заинтересованные стороны"},
        definitions={
            "ko": "기업 활동에 영향을 주거나 영향을 받는 주주, 노동자, 소비자, 협력업체, 지역사회 등의 개인과 집단입니다.",
            "es": "Son las personas o grupos que influyen en una empresa o se ven afectados por ella, como accionistas, trabajadores, consumidores, proveedores y comunidades locales.",
            "ru": "Это люди и группы, которые влияют на деятельность компании или испытывают ее влияние: акционеры, работники, потребители, поставщики и местные сообщества.",
        },
        aliases=["이해관계자", "stakeholder", "stakeholders", "grupos de interés", "partes interesadas", "заинтересованные стороны", "стейкхолдер"],
    ),
    "anti_corruption": ESGTerm(
        category="G",
        names={"ko": "부패 방지", "es": "lucha contra la corrupción", "ru": "противодействие коррупции"},
        definitions={
            "ko": "뇌물, 횡령, 부정청탁과 같은 부정행위를 예방하고 발견하며 책임을 묻기 위한 제도와 활동입니다.",
            "es": "Son las políticas y acciones destinadas a prevenir, detectar y sancionar prácticas como el soborno, la malversación y otras conductas indebidas.",
            "ru": "Это меры и правила для предотвращения, выявления и наказания взяточничества, хищений и других коррупционных действий.",
        },
        aliases=["부패 방지", "반부패", "anti corruption", "anticorruption", "lucha contra la corrupción", "anticorrupción", "противодействие коррупции", "борьба с коррупцией"],
    ),
}


EXAMPLE_QUESTIONS = {
    "ko": ["ESG 경영이 뭐야?", "탄소중립을 설명해 줘", "이해관계자가 무엇인가요?"],
    "es": ["¿Qué es la gestión ESG?", "Explica la neutralidad de carbono", "¿Qué son los grupos de interés?"],
    "ru": ["Что такое ESG?", "Объясни углеродную нейтральность", "Кто такие заинтересованные стороны?"],
}


def normalize(text: str) -> str:
    punctuation = "?!¿¡.,:;()[]{}'\"/\\-_"
    normalized = text.lower().strip()
    for char in punctuation:
        normalized = normalized.replace(char, " ")
    return " ".join(normalized.split())


def find_term(user_text: str) -> Optional[str]:
    query = normalize(user_text)

    # 1. Exact or contained alias match
    candidates = []
    for key, term in TERMS.items():
        for alias in term.aliases + list(term.names.values()):
            normalized_alias = normalize(alias)
            if normalized_alias and normalized_alias in query:
                candidates.append((len(normalized_alias), key))

    if candidates:
        return max(candidates)[1]

    # 2. Fuzzy match for short term-like inputs
    aliases_to_key: Dict[str, str] = {}
    for key, term in TERMS.items():
        for alias in term.aliases + list(term.names.values()):
            aliases_to_key[normalize(alias)] = key

    close = get_close_matches(query, aliases_to_key.keys(), n=1, cutoff=0.70)
    return aliases_to_key[close[0]] if close else None


def answer_for(term_key: str, language: str) -> str:
    term = TERMS[term_key]
    ui = UI_TEXT[language]
    category = CATEGORY_NAMES[term.category][language]
    return (
        f"**{ui['category']}**: {category}\n\n"
        f"**{ui['term']}**: {term.names[language]}\n\n"
        f"**{ui['definition']}**: {term.definitions[language]}"
    )


def fallback_answer(language: str) -> str:
    ui = UI_TEXT[language]
    examples = ", ".join(term.names[language] for term in list(TERMS.values())[:7])
    return f"{ui['not_found']}\n\n{ui['suggestion']} {examples}"


st.set_page_config(
    page_title="Multilingual ESG Chatbot",
    page_icon="🌱",
    layout="centered",
)

# Sidebar
with st.sidebar:
    selected_language_name = st.selectbox(
        "Language / Idioma / Язык",
        list(LANGUAGES.keys()),
        index=0,
    )
    language = LANGUAGES[selected_language_name]
    ui = UI_TEXT[language]

    st.subheader(ui["examples"])
    for example in EXAMPLE_QUESTIONS[language]:
        st.caption(f"• {example}")

    with st.expander(ui["supported"]):
        for category in ["E", "S", "G", "ESG"]:
            terms = [
                term.names[language]
                for term in TERMS.values()
                if term.category == category
            ]
            if terms:
                st.markdown(f"**{CATEGORY_NAMES[category][language]}**")
                st.write(" · ".join(terms))

    if st.button(ui["reset"], use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main area
st.title(ui["title"])
st.write(ui["subtitle"])
st.info(ui["disclaimer"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(ui["welcome"])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(ui["input"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    term_key = find_term(prompt)
    response = answer_for(term_key, language) if term_key else fallback_answer(language)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
