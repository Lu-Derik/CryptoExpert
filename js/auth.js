// Supabase Configuration
// Replace with your own Supabase project URL and Anon Key
const SUPABASE_URL = 'https://zfufmedufgrayhgdkufc.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmdWZtZWR1ZmdyYXloZ2RrdWZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyOTg0OTcsImV4cCI6MjA4NDg3NDQ5N30.ZkFUW7xfj74vakucwA7Q3aaHCpIkshVU_YeF_tesLfs';

const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Auth UI Logic
const authModal = document.getElementById('auth-modal');
const loginBtn = document.getElementById('login-btn');
const joinBtn = document.getElementById('join-btn');
const closeModal = document.getElementById('close-modal');
const authForm = document.getElementById('auth-form');
const authTitle = document.getElementById('auth-title');
const authSubmitBtn = document.getElementById('auth-submit-btn');
const toggleAuthMode = document.getElementById('toggle-auth-mode');

let isLoginMode = true;

// Open modal
const openModal = (mode) => {
    isLoginMode = mode === 'login';
    authTitle.innerText = isLoginMode ? 'Welcome Back' : 'Create Account';
    authSubmitBtn.innerText = isLoginMode ? 'Login' : 'Sign Up';
    toggleAuthMode.innerText = isLoginMode ? "Don't have an account? Join" : "Already have an account? Login";
    authModal.classList.remove('hidden');
    authModal.classList.add('flex');
};

loginBtn?.addEventListener('click', () => openModal('login'));
joinBtn?.addEventListener('click', () => openModal('join'));

// Close modal
closeModal?.addEventListener('click', () => {
    authModal.classList.add('hidden');
    authModal.classList.remove('flex');
});

// Toggle mode
toggleAuthMode?.addEventListener('click', (e) => {
    e.preventDefault();
    openModal(isLoginMode ? 'join' : 'login');
});

// Handle Form Submission
authForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email-input').value;
    const password = document.getElementById('password-input').value;

    try {
        let result;
        if (isLoginMode) {
            result = await supabaseClient.auth.signInWithPassword({ email, password });
        } else {
            result = await supabaseClient.auth.signUp({ email, password });
        }

        if (result.error) throw result.error;

        alert(isLoginMode ? 'Logged in successfully!' : 'Check your email for confirmation!');
        authModal.classList.add('hidden');
        updateUserUI(result.data.user);
    } catch (error) {
        alert(error.message);
    }
});

// Update UI based on user status
const updateUserUI = (user) => {
    const authSection = document.getElementById('auth-section');
    if (user) {
        authSection.innerHTML = `
            <div class="flex items-center space-x-4">
                <span class="text-sm font-medium text-gray-500">${user.email}</span>
                <button id="logout-btn" class="px-6 py-2.5 rounded-full border border-gray-300 dark:border-gray-700 font-medium text-sm hover:bg-white dark:hover:bg-gray-800 transition-colors">Logout</button>
            </div>
        `;
        document.getElementById('logout-btn')?.addEventListener('click', async () => {
            await supabaseClient.auth.signOut();
            window.location.reload();
        });
    }
};

// Check initial session
window.addEventListener('DOMContentLoaded', async () => {
    const { data: { session } } = await supabaseClient.auth.getSession();
    if (session) updateUserUI(session.user);
});
