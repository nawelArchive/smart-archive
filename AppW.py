import streamlit as st
import pandas as pd
import datetime
# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Smart Archive - Modèle Physique",
    page_icon="📁",
    layout="wide"
)

# ---------------------------------------------------------
# إدارة حالة تسجيل الدخول (Session State)
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False  # القيمة الافتراضية غير مسجل الدخول

# ---------------------------------------------------------
# الشاشة الأولى: نموذج تسجيل الدخول (إذا لم يسجل الدخول بعد)
# ---------------------------------------------------------
if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول إلى النظام</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم (Nom d'utilisateur)")
            password = st.text_input("كلمة المرور (Mot de passe)", type="password")
           
            
            # 👈 ضع الكود الجديد هنا مباشرة مع نفس محاذاة الأسطر (4 مسافات)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    headers = st.context.headers
                    user_ip = headers.get("X-Forwarded-For", "Unknown IP")
                    ua = headers.get("User-Agent", "")
            
            # تحديد نوع الجهاز/النظام
                    if "Android" in ua:
                        os_name = "الهاتف (Android)"
                    elif "iPhone" in ua:
                        os_name = "الهاتف (iPhone)"
                    elif "Windows" in ua:
                        os_name = "كمبيوتر (Windows)"
                    elif "Macintosh" in ua:
                        os_name = "كمبيوتر (Mac)"
                    elif "Linux" in ua:
                        os_name = "كمبيوتر (Linux)"
                    else:
                        os_name = "جهاز غير معروف"

            # تحديد نوع المتصفح
                    if "Firefox" in ua:
                        browser = "Firefox"
                    elif "Edg" in ua:
                     browser = "Edge"
                    elif "Chrome" in ua:
                      browser = "Chrome"
                    elif "Safari" in ua:
                      browser = "Safari"
                    else:
                      browser = "متصفح آخر"

                    device_info = f"{os_name} - {browser}"
                    log_entry = f"الوقت: {now} | IP: {user_ip} | الجهاز: {device_info}\n"


                    with open("visitor_logs.txt", "a", encoding="utf-8") as f:
                        f.write(log_entry)

                    st.success("تم تسجيل الدخول بنجاح")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    st.stop()  # يمنع إكمال بقية الكود قبل تسجيل الدخول

# ---------------------------------------------------------
# الشاشة الرئيسية التطبيق (تظهر فقط بعد تسجيل الدخول)
# ---------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'> Smart Archive </h1>", unsafe_allow_html=True)

# القائمة الجانبية
st.sidebar.title("📌 القائمة الرئيسية")
st.sidebar.markdown("---")

menu = st.sidebar.radio("اختر الشاشة المراد عرضها:", [
    "🌐 Schéma des Relations (Diagramme)",
    "📊 Structure des tables"
])

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Actualiser البيانات"):
    st.toast("تم تحديث الواجهة بنجاح!", icon="🎉")

# زر الخروج المنفذ بشكل صحيح
if st.sidebar.button("⏹ Déconnexion"):
    st.session_state.clear()
    st.session_state["logged_in"] = False
    st.rerun()


# ==========================================
# الشاشة الأولى: المخطط الرأسي (Graphviz)
# ==========================================
if menu == "🌐 Schéma des Relations (Diagramme)":
    st.subheader("🌐 Diagramme ERD (مخطط العلاقات الشامل)")
    
    view_type = st.radio("اختر نمط عرض المخطط:", ["Vertical (مطابق للصورة 📐)", "Horizontal (عرض عريض ↔️)"], horizontal=True)
    rank_dir = "TB" if "Vertical" in view_type else "LR"

    dot_code = f"""
    digraph G {{
        rankdir={rank_dir};
        node [shape=rect, style="filled,rounded", fontname="Arial Bold", fontsize=10, height=0.5, width=1.6];
        edge [fontname="Arial", fontsize=8, color="#475569", penwidth=1.5];
        
        // Metier
        node [fillcolor="#DBEAFE", color="#2563EB", fontcolor="#1E3A8A"];
        Boite [label="Boites_Archive"];
        Docu [label="Documents"];
        Cate [label="Categories"];
        Mouv [label="Mouvement_Archive"];
        Digit [label="Digital_Files"];
        Empl [label="Employees"];
        Param [label="Parametres"];

        // Geographie
        node [fillcolor="#DCFCE7", color="#16A34A", fontcolor="#14532D"];
        Wilay [label="Wilayas"];
        Daira [label="Dairas"];
        Com [label="Communes"];

        // Securite
        node [fillcolor="#F3E8FF", color="#9333EA", fontcolor="#581C87"];
        Utilis [label="Utilisateurs"];
        Auto [label="Autorisations"];
        Menu [label="Menus"];
        Oper [label="Operations"];
        Mappa [label="Mappage_Autorisations"];

        // Audit
        node [fillcolor="#FFEDD5", color="#EA580C", fontcolor="#7C2D12"];
        EmpAudit [label="Employees_Audit"];
        ErrAudit [label="Erreurs_Audit"];

        // Relationships
        Boite -> Docu;
        Docu -> Cate;
        Docu -> Mouv;
        Docu -> Digit;
        
        Utilis -> Docu;
        Utilis -> Mouv;
        Utilis -> Auto;
        
        Mouv -> Empl;
        Empl -> Com;
        Com -> Daira;
        Daira -> Wilay;
        
        Auto -> Menu;
        Auto -> Oper;
        Oper -> Mappa;
        Menu -> Mappa;

        Empl -> EmpAudit [style=dashed];
        Utilis -> ErrAudit [style=dashed];
    }}
    """
    st.graphviz_chart(dot_code)

# ==========================================
# الشاشة الثانية: الجداول الـ 17 كاملة
# ==========================================
elif menu == "📊 Structure des tables":
    st.subheader("📊 عرض هيكلة الجداول والأعمدة (17 جدول كاملة)")
    
    table_list = [
        "Audit.Employees_Audit",
        "Audit.Erreurs_Audit",
        "Geographie.Communes",
        "Geographie.Dairas",
        "Geographie.Wilayas",
        "Metier.Boites_Archive",
        "Metier.Categories",
        "Metier.Digital_Files",
        "Metier.Documents",
        "Metier.Employees",
        "Metier.Mouvement_Archive",
        "Metier.Parametres",
        "Securite.Autorisations",
        "Securite.Mappage_Autorisations",
        "Securite.Menus",
        "Securite.Operations",
        "Securite.Utilisateurs"
    ]
    
    selected_table = st.selectbox("اختر الجدول لعرض التفاصيل:", table_list)

    data_dict = {
        "Audit.Employees_Audit": [
            {"Colonne": "ID_Audit_Emp", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "ID_Employee", "Type": "int", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Code_Employees", "Type": "char(6)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Nom_E", "Type": "varchar(50)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Prenom_E", "Type": "varchar(50)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Type_MAJ", "Type": "varchar(20)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Date_MAJ", "Type": "datetime", "Cle": "-", "Null": "non NULL"}
        ],
        "Audit.Erreurs_Audit": [
            {"Colonne": "ID_Erreur", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_Procedure", "Type": "nvarchar(128)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Message_Erreur", "Type": "nvarchar(max)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Date_Erreur", "Type": "datetime", "Cle": "-", "Null": "non NULL"}
        ],
        "Geographie.Communes": [
            {"Colonne": "ID_Commune", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Code_Commune", "Type": "varchar(6)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "ID_Daira", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "Nom_Commune_Fr", "Type": "varchar(30)", "Cle": "-", "Null": "non NULL"}
        ],
        "Geographie.Dairas": [
            {"Colonne": "ID_Daira", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Code_Daira", "Type": "varchar(5)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "ID_Wilaya", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "Nom_Daira_Fr", "Type": "varchar(30)", "Cle": "-", "Null": "non NULL"}
        ],
        "Geographie.Wilayas": [
            {"Colonne": "ID_Wilaya", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Code_Wilaya", "Type": "varchar(4)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Nom_Wilaya_Fr", "Type": "varchar(30)", "Cle": "-", "Null": "non NULL"}
        ],
        "Metier.Boites_Archive": [
            {"Colonne": "ID_Boite", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Code_Boite", "Type": "varchar(7)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Nom_B", "Type": "varchar(20)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Emplacement", "Type": "varchar(100)", "Cle": "-", "Null": "non NULL"}
        ],
        "Metier.Categories": [
            {"Colonne": "ID_Categorie", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_Cat", "Type": "varchar(100)", "Cle": "-", "Null": "non NULL"}
        ],
        "Metier.Digital_Files": [
            {"Colonne": "ID_DigitalFile", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_Fichier", "Type": "varchar(255)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Chemin_Acces", "Type": "varchar(500)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "ID_Document", "Type": "int", "Cle": "FK", "Null": "non NULL"}
        ],
        "Metier.Documents": [
            {"Colonne": "ID_Document", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Titre", "Type": "varchar(150)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "ID_Boite", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "ID_Categorie", "Type": "int", "Cle": "FK", "Null": "non NULL"}
        ],
        "Metier.Employees": [
            {"Colonne": "ID_Employee", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_E", "Type": "varchar(20)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Prenom_E", "Type": "varchar(30)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "ID_Commune", "Type": "int", "Cle": "FK", "Null": "non NULL"}
        ],
        "Metier.Mouvement_Archive": [
            {"Colonne": "ID_Mouvement", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "ID_Document", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "Type_Mouvement", "Type": "varchar(50)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "ID_Employee", "Type": "int", "Cle": "FK", "Null": "non NULL"}
        ],
        "Metier.Parametres": [
            {"Colonne": "ID_Parametre", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_Parametre", "Type": "varchar(50)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Valeur_Parametre", "Type": "nvarchar(max)", "Cle": "-", "Null": "non NULL"}
        ],
        "Securite.Autorisations": [
            {"Colonne": "ID_Autorisation", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "ID_Utilisateur", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "ID_Menu", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "ID_Operation", "Type": "int", "Cle": "FK", "Null": "non NULL"}
        ],
        "Securite.Mappage_Autorisations": [
            {"Colonne": "ID_Mappage_Autorisations", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "ID_Menu", "Type": "int", "Cle": "FK", "Null": "non NULL"},
            {"Colonne": "ID_Operation", "Type": "int", "Cle": "FK", "Null": "non NULL"}
        ],
        "Securite.Menus": [
            {"Colonne": "ID_Menu", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_Menu", "Type": "varchar(30)", "Cle": "-", "Null": "non NULL"}
        ],
        "Securite.Operations": [
            {"Colonne": "ID_Operation", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Nom_Operation", "Type": "varchar(30)", "Cle": "-", "Null": "non NULL"}
        ],
        "Securite.Utilisateurs": [
            {"Colonne": "ID_Utilisateur", "Type": "int", "Cle": "PK", "Null": "non NULL"},
            {"Colonne": "Login_U", "Type": "varchar(20)", "Cle": "-", "Null": "non NULL"},
            {"Colonne": "Date_Creation", "Type": "datetime", "Cle": "-", "Null": "non NULL"}
        ]
    }

    df = pd.DataFrame(data_dict.get(selected_table, []))
    st.dataframe(df)

    st.sidebar.title("سجل الزوار")

# زر لمسح ملف السجل بضغطة واحدة
    if st.sidebar.button("🗑️ مسح سجل الزوار"):
         open("visitor_logs.txt", "w", encoding="utf-8").close()
         st.sidebar.success("تم مسح السجل بنجاح!")
         st.rerun()

# عرض محتوى السجل
    try:
        with open("visitor_logs.txt", "r", encoding="utf-8") as f:
            logs = f.read()
            st.sidebar.text_area("تفاصيل الزوار:", value=logs, height=300)
    except FileNotFoundError:
        st.sidebar.write("السجل فارغ حالياً.")



