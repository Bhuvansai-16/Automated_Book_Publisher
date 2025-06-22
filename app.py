import streamlit as st
from scraper import scrape_chapter
from rewrite_engine import run_agents
from chroma_manager import save_version, list_versions
import asyncio

# Page config
st.set_page_config(page_title="AI Book Workflow", layout="wide")

# Initialize session state defaults
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = {}
if 'display' not in st.session_state:
    st.session_state['display'] = None
if 'onboarded' not in st.session_state:
    st.session_state['onboarded'] = False
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = '🔧 Scrape & Rewrite'

# User login (first page before onboarding)
if 'user_id' not in st.session_state:
    st.title("Hey there! 👋  Welcome to Automated Book Publication workflow" )
    st.title("🔐 User Login")
    username = st.text_input("Enter your name to get started:")
    if st.button("Login") and username:
        st.session_state['user_id'] = username
        st.rerun()
    st.stop()

user_id = st.session_state['user_id']

# Onboarding screen
if not st.session_state['onboarded']:
    st.title(f"🚀 Welcome, {user_id}")
    st.markdown(
        "This app lets you:\n"
        "1. Scrape chapter content from a web URL.\n"
        "2. Run a multi-stage AI rewrite pipeline (Writer → Editor → Reviewer).\n"
        "3. Save and manage multiple versions of your chapters.\n"
        "4. Read and rate saved chapters.\n\n"
        "Click **Get Started** to begin!"
    )
    if st.button("Get Started"):
        st.session_state['onboarded'] = True
        st.rerun()
    st.stop()

# Helper: group saved versions by book and sorted chapters
# and apply simple RL-based ranking based on user feedback
def group_versions(versions):
    books = {}
    for item in versions:
        books.setdefault(item['book'], []).append({'chapter': item['chapter'], 'content': item['content']})
    for book, chaps in books.items():
        chaps.sort(key=lambda x: int(''.join(filter(str.isdigit, x['chapter'])) or 0))
    feedbacks = st.session_state.get('feedbacks', {})
    book_scores = {b: (sum(feedbacks[b]) / len(feedbacks[b])) if feedbacks.get(b) else 0 for b in books}
    ranked = sorted(books.keys(), key=lambda b: book_scores.get(b, 0), reverse=True)
    return {b: books[b] for b in ranked}

# Fetch and rank saved versions for the current user
versions = list_versions(user_id=user_id)
books = group_versions(versions)
show_reader = st.session_state['display'] is not None

# Sidebar: Profile and book access
st.sidebar.title(f"👋 Hey, {user_id}")
st.sidebar.title("📚 Saved Books & Chapters")
search_term = st.sidebar.text_input("Search Books", key='search_book')
filtered_books = [b for b in books.keys() if search_term.lower() in b.lower()] if search_term else list(books.keys())
if filtered_books:
    sb = st.sidebar.selectbox("Book", filtered_books, key='sb_book')
    chaps = books[sb]
    sel = st.sidebar.selectbox("Chapter", [c['chapter'] for c in chaps], key='sb_chap')
    if st.sidebar.button("Read Chapter"):
        st.session_state['display'] = {
            'book': sb,
            'chapter': sel,
            'content': next(c['content'] for c in chaps if c['chapter'] == sel)
        }
        st.session_state['active_tab'] = '📖 Reader'
        st.rerun()
else:
    st.sidebar.info("No books match your search." if search_term else "No saved versions yet. Save a chapter to begin reading.")

st.sidebar.markdown("""
<span title='Your saved, readable chapters will appear here after selection.' style='color:gray;'>ℹ️ Tip: Switch to Reader only when you want to read a saved chapter.</span>
""", unsafe_allow_html=True)
tabs = ['🔧 Scrape & Rewrite', '🗂️ My Library'] + (['📖 Reader'] if show_reader else [])
current_tab = st.session_state['active_tab'] if st.session_state['active_tab'] in tabs else tabs[0]
st.session_state['active_tab'] = st.sidebar.radio("Mode", tabs, index=tabs.index(current_tab))

# Scrape & Rewrite Tab
if st.session_state['active_tab'] == '🔧 Scrape & Rewrite':
    st.title("📘 Automated Book Publication Workflow")
    st.subheader("Fetch & Rewrite Pipeline")

    url = st.text_input("Chapter URL to Scrape", placeholder="Enter a valid Wikisource URL", key='url_input')
    if url:
        if not (url.startswith("http://") or url.startswith("https://")):
            st.error("Please enter a valid URL starting with http:// or https://")
            st.stop()

    if st.button("Scrape Chapter", key='scrape_btn'):
        st.session_state['original'] = scrape_chapter(url)
        st.success("Chapter scraped successfully!")

    if st.session_state.get('original'):
        st.subheader("Original Chapter")
        st.text_area("", st.session_state['original'], height=250, key='orig_area')
        if st.button("Run Rewrite Agent", key='rewrite_btn'):
            with st.spinner("AI Writer → Editor → Reviewer working..."):
                res = asyncio.run(run_agents(st.session_state['original']))
                st.session_state['rewritten'] = res['reviewed']
                st.success("AI rewrite complete!")

    if st.session_state.get('rewritten'):
        st.subheader("AI Rewrite (Editable)")
        st.session_state['edited'] = st.text_area("", st.session_state['rewritten'], height=300, key='edit_area')
        st.markdown("#### Save Final Version & Next Chapter Options")
        col1, col2 = st.columns(2)
        with col1:
            b = st.text_input("Book Title", value="The Gates of Morning", key='save_book')
        with col2:
            c = st.text_input("Chapter Title", value="Book 1 - Chapter 1", key='save_chap')
        save = st.button("Save Final Version", key='save_btn')
        nxt = st.button("Add Next Chapter", key='next_btn')
        if save:
            save_version(b, c, st.session_state['edited'], user_id)
            st.success(f"Saved '{c}' under '{b}'.")
            for k in ['url_input','original','rewritten','edited','save_book','save_chap']:
                st.session_state.pop(k, None)
            st.session_state['active_tab'] = '🔧 Scrape & Rewrite'
            st.rerun()
        if nxt:
            for k in ['original','rewritten','edited','save_book','save_chap']:
                st.session_state.pop(k, None)
            st.success("Ready for next chapter. Enter new URL above.")

elif st.session_state['active_tab'] == '📖 Reader':
    disp = st.session_state['display']
    st.header(f"{disp['book']} - {disp['chapter']}")
    st.text_area("", disp['content'], height=400, key='reader_area')
    st.markdown("**Rate this chapter (1–10):**")
    rating = st.select_slider("", options=list(range(1,11)), value=5, key='rating')
    if st.button("Submit Rating", key='rate_btn'):
        fb = st.session_state['feedbacks'].setdefault(disp['book'], [])
        fb.append(rating)
        st.success(f"Rating submitted: {rating}/10!")

    if st.button("📥 Download Full Book"):
        full_text = f"{disp['book']}\n\n"
        for chapter in books[disp['book']]:
            full_text += f"{chapter['chapter']}\n{'-'*40}\n{chapter['content']}\n\n"
        st.download_button(
            label="Download Complete Book",
            data=full_text,
            file_name=f"{disp['book'].replace(' ', '_')}.txt",
            mime="text/plain",
        )

    idx = [c['chapter'] for c in books[disp['book']]].index(disp['chapter'])
    colp, coln = st.columns(2)
    with colp:
        if st.button("Previous Chapter") and idx>0:
            prev = books[disp['book']][idx-1]['chapter']
            st.session_state['display']['chapter'] = prev
            st.rerun()
    with coln:
        if st.button("Next Chapter") and idx< len(books[disp['book']])-1:
            nxtc = books[disp['book']][idx+1]['chapter']
            st.session_state['display']['chapter'] = nxtc
            st.rerun()

elif st.session_state['active_tab'] == '🗂️ My Library':
    st.title("🗂️ My Book Library")
    for book, chapters in books.items():
        with st.expander(f"📘 {book} ({len(chapters)} chapters)"):
            for chap in chapters:
                st.markdown(f"**📖 {chap['chapter']}**")
                st.markdown(f"<div style='padding-left:1rem;'>{chap['content'][:200]}...</div>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button(f"Read {chap['chapter']}", key=f"dashread_{book}_{chap['chapter']}"):
                        st.session_state['display'] = {
                            'book': book,
                            'chapter': chap['chapter'],
                            'content': chap['content']
                        }
                        st.session_state['active_tab'] = '📖 Reader'
                        st.rerun()
                with col2:
                    st.caption("Click 'Read' to open chapter in Reader mode")
