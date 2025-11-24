import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { questionsAPI } from '../api/questions';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

const AskQuestion = () => {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      toast.error('Title is required');
      return;
    }

    setLoading(true);

    try {
      const question = await questionsAPI.create({ title, body });
      toast.success('Question posted successfully!');
      navigate(`/questions/${question.id}`);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to post question');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Ask a Question</h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="What's your programming question?"
            />
            <p className="mt-1 text-sm text-gray-500">
              Be specific and imagine you're asking another person
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Body (Optional)
            </label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={8}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Include all the information someone would need to answer your question..."
            />
            <p className="mt-1 text-sm text-gray-500">
              Add more details, code snippets, or context
            </p>
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Posting...' : 'Post Question'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AskQuestion;
