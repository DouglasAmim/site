// script.js
document.addEventListener('DOMContentLoaded', () => {
    // Carrega tarefas do localStorage
    loadTasks();
    loadRanking();

    // Formulário de nova tarefa
    const taskForm = document.getElementById('task-form');
    if(taskForm) {
        taskForm.addEventListener('submit', handleSubmit);
    }
});

function handleSubmit(e) {
    e.preventDefault();
    
    // Captura localização
    navigator.geolocation.getCurrentPosition(position => {
        const task = {
            id: Date.now(),
            nome: document.getElementById('nome').value,
            tipo: document.getElementById('tipo-tarefa').value,
            descricao: document.getElementById('descricao').value,
            foto: document.getElementById('foto').files[0],
            location: {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            },
            data: new Date().toISOString(),
            concluida: false
        };

        saveTask(task);
        alert('Tarefa enviada com sucesso!');
        window.location.href = 'index.html';
    }, error => {
        alert('É necessário permitir a localização para enviar a tarefa!');
    });
}

function saveTask(task) {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.push(task);
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function loadTasks() {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    
    // Carrega tarefas pendentes
    const pendingContainer = document.getElementById('pending-tasks');
    const completedContainer = document.getElementById('completed-tasks');
    
    if(pendingContainer && completedContainer) {
        pendingContainer.innerHTML = '';
        completedContainer.innerHTML = '';
        
        tasks.forEach(task => {
            const html = `
                <div class="task-card">
                    <h3>${task.tipo} pontos</h3>
                    <p>${task.descricao}</p>
                    <small>Por: ${task.nome}</small>
                </div>
            `;
            
            if(task.concluida) {
                completedContainer.innerHTML += html;
            } else {
                pendingContainer.innerHTML += html;
            }
        });
    }
}

function loadRanking() {
    const rankingContainer = document.getElementById('ranking-list');
    if(rankingContainer) {
        const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        const ranking = {};
        
        tasks.forEach(task => {
            if(task.concluida) {
                if(!ranking[task.nome]) ranking[task.nome] = 0;
                ranking[task.nome] += parseInt(task.tipo);
            }
        });
        
        const sorted = Object.entries(ranking)
            .sort((a, b) => b[1] - a[1])
            .map(([nome, pontos]) => `
                <div class="ranking-item">
                    <span>${nome}</span>
                    <span>${pontos} pontos</span>
                </div>
            `).join('');
        
        rankingContainer.innerHTML = sorted;
    }
}