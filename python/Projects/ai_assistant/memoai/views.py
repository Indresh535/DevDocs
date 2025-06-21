
# Create your views here.
from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm, QuestionForm
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load embedding model and index
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
note_map = {}

def home(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'notes': notes})

def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            # Add to vector index
            embedding = model.encode([note.content])[0]
            index.add(np.array([embedding], dtype='float32'))
            note_map[index.ntotal - 1] = note
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})

def ask_question(request):
    answer = None
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            query_embedding = model.encode([question])
            D, I = index.search(np.array(query_embedding, dtype='float32'), k=3)
            top_notes = [note_map.get(i) for i in I[0] if i in note_map]
            combined_context = "\n".join([n.content for n in top_notes if n])
            # Simple LLM-like answer (replace this with OpenAI later)
            answer = f"Based on your notes:\n{combined_context}"
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form, 'answer': answer})

