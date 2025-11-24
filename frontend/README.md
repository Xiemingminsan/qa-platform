# Q&A Platform - Frontend

React + TypeScript + Vite frontend for the Q&A Platform.

## 🛠️ Technology Stack

- **Framework:** React 18
- **Language:** TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **State Management:** Context API
- **Notifications:** react-hot-toast

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/               # API client functions
│   │   ├── axios.ts       # Axios instance & interceptors
│   │   ├── auth.ts        # Authentication API
│   │   ├── questions.ts   # Questions API
│   │   ├── answers.ts     # Answers API
│   │   └── votes.ts       # Voting API
│   ├── components/        # Reusable components
│   │   ├── Navbar.tsx
│   │   ├── QuestionCard.tsx
│   │   ├── AnswerCard.tsx
│   │   └── VoteButton.tsx
│   ├── context/           # React Context
│   │   └── AuthContext.tsx
│   ├── pages/             # Page components
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── AskQuestion.tsx
│   │   └── QuestionDetail.tsx
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── public/                # Static assets
├── index.html             # HTML template
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── vite.config.ts         # Vite config
├── tailwind.config.js     # Tailwind config
└── .env.example           # Environment variables template
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend README)

### Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

   The app will open at: http://localhost:5174

## 📱 Features

### User Features
- User registration and login
- Browse all questions
- Search questions by keyword
- View question details with answers
- Ask new questions
- Post answers to questions
- Upvote/downvote questions and answers
- Edit own questions and answers
- Delete own content

### UI/UX Features
- Responsive design (mobile-friendly)
- Toast notifications for user feedback
- Loading states
- Clean, professional interface
- Intuitive navigation

## 🎨 Pages

### Home (`/`)
- List of all questions
- Search functionality
- Question stats (votes, answers, views)
- Links to question details

### Login (`/login`)
- Email and password login form
- Link to registration page
- JWT token handling

### Register (`/register`)
- User registration form
- Username, email, password fields
- Link to login page

### Ask Question (`/ask`)
- Create new question form
- Title and body fields
- Requires authentication

### Question Detail (`/questions/:id`)
- Full question display
- All answers
- Vote buttons
- Post answer form
- Edit/delete own content

## 🔌 API Integration

All API calls go through the Axios instance in `src/api/axios.ts`:

- Automatically adds JWT token to requests
- Handles authentication headers
- Centralized error handling

### Example API Usage

```typescript
// In a component
import { questionsAPI } from '../api/questions';

const fetchQuestions = async () => {
  const questions = await questionsAPI.getAll();
  setQuestions(questions);
};
```

## 🔐 Authentication

Authentication is managed via Context API (`AuthContext`):

```typescript
// In a component
import { useAuth } from '../context/AuthContext';

const MyComponent = () => {
  const { user, isAuthenticated, login, logout } = useAuth();

  // Use authentication state and methods
};
```

JWT token is stored in localStorage and automatically included in API requests.

## 🎨 Styling

TailwindCSS utility classes are used throughout:

```tsx
<button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
  Click me
</button>
```

## 📦 Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

## 🚀 Deployment (Vercel)

### Steps:

1. **Push to GitHub**
   - Ensure your code is pushed to GitHub

2. **Create Vercel Account**
   - Go to [Vercel.com](https://vercel.com)
   - Sign up with GitHub

3. **Import Project**
   - Click "New Project"
   - Import your frontend repository
   - Vercel auto-detects Vite configuration

4. **Configure Environment Variables**
   - Add `VITE_API_URL` with your deployed backend URL
   - Example: `https://your-backend.railway.app`

5. **Deploy**
   - Click "Deploy"
   - Vercel builds and deploys automatically
   - Get your live URL: `https://your-app.vercel.app`

6. **Update Backend CORS**
   - Add your Vercel URL to backend CORS origins
   - Redeploy backend if needed

## 🧪 Testing

### Manual Testing Checklist

- [ ] Register new user
- [ ] Login with credentials
- [ ] View questions list
- [ ] Search questions
- [ ] Create new question
- [ ] View question details
- [ ] Post answer
- [ ] Upvote/downvote question
- [ ] Upvote/downvote answer
- [ ] Edit own question
- [ ] Delete own question
- [ ] Edit own answer
- [ ] Delete own answer
- [ ] Logout

### Testing with Backend

Ensure backend is running at the URL specified in `.env`:

```bash
# Backend should be running
# Start frontend
npm run dev
```

## 📝 Environment Variables

```env
# Required
VITE_API_URL=http://localhost:8000

# For production (example)
# VITE_API_URL=https://your-backend.railway.app
```

## 🔧 Common Issues

### CORS Errors
- Ensure backend CORS settings include your frontend URL
- Check `BACKEND_CORS_ORIGINS` in backend `.env`

### API Not Found
- Verify `VITE_API_URL` in `.env`
- Ensure backend is running
- Check network tab in browser DevTools

### Build Errors
- Delete `node_modules/` and `package-lock.json`
- Run `npm install` again
- Clear Vite cache: `rm -rf .vite`

## 📄 License

This is a student project for educational purposes.

---

**Need help?** Check the main project README or backend documentation.
