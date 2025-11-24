import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { questionsAPI } from '../api/questions';
import { answersAPI } from '../api/answers';
import { Question, Answer } from '../types';
import { useAuth } from '../context/AuthContext';
import VoteButton from '../components/VoteButton';
import AnswerCard from '../components/AnswerCard';
import toast from 'react-hot-toast';

const QuestionDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();
  const [question, setQuestion] = useState<Question | null>(null);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [answerBody, setAnswerBody] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editBody, setEditBody] = useState('');
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    if (id) {
      fetchData();
    }
  }, [id]);

  useEffect(() => {
    if (question) {
      setEditTitle(question.title);
      setEditBody(question.body || '');
    }
  }, [question]);

  const fetchData = async () => {
    if (!id) return;

    setLoading(true);
    try {
      const [questionData, answersData] = await Promise.all([
        questionsAPI.getById(parseInt(id)),
        answersAPI.getByQuestionId(parseInt(id)),
      ]);
      setQuestion(questionData);
      setAnswers(answersData);
    } catch (error) {
      toast.error('Failed to load question');
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!isAuthenticated) {
      toast.error('Please login to answer');
      navigate('/login');
      return;
    }

    if (!answerBody.trim()) {
      toast.error('Answer cannot be empty');
      return;
    }

    setSubmitting(true);
    try {
      await answersAPI.create(parseInt(id!), answerBody);
      toast.success('Answer posted!');
      setAnswerBody('');
      fetchData();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to post answer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateQuestion = async () => {
    if (!editTitle.trim()) {
      toast.error('Title cannot be empty');
      return;
    }

    setUpdating(true);
    try {
      const updatedQuestion = await questionsAPI.update(question!.id, {
        title: editTitle,
        body: editBody || undefined,
      });
      setQuestion(updatedQuestion);
      toast.success('Question updated');
      setIsEditing(false);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update question');
    } finally {
      setUpdating(false);
    }
  };

  const handleDeleteQuestion = async () => {
    if (!confirm('Are you sure you want to delete this question?')) return;

    try {
      await questionsAPI.delete(question!.id);
      toast.success('Question deleted');
      navigate('/');
    } catch (error) {
      toast.error('Failed to delete question');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!question) {
    return null;
  }

  const isOwner = user && user.username === question.author_username;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Question */}
      <div className="bg-white p-8 rounded-lg shadow-md mb-6">
        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-6">
          <span>Asked by <strong>{question.author_username}</strong></span>
          <span>{formatDate(question.created_at)}</span>
          <span>{question.view_count} views</span>
        </div>

        <div className="flex space-x-6">
          <VoteButton
            itemId={question.id}
            itemType="question"
            initialScore={question.vote_score}
            onVote={fetchData}
          />

          <div className="flex-1">
            {isEditing ? (
              <div>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full p-3 border rounded-lg mb-4 text-2xl font-bold"
                  placeholder="Question title"
                />
                <textarea
                  value={editBody}
                  onChange={(e) => setEditBody(e.target.value)}
                  className="w-full p-3 border rounded-lg"
                  rows={6}
                  placeholder="Question body (optional)"
                />
                <div className="mt-4 space-x-2">
                  <button
                    onClick={handleUpdateQuestion}
                    disabled={updating}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                  >
                    {updating ? 'Saving...' : 'Save'}
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setEditTitle(question.title);
                      setEditBody(question.body || '');
                    }}
                    disabled={updating}
                    className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">{question.title}</h1>
                {question.body && (
                  <p className="text-gray-800 whitespace-pre-wrap mb-4">{question.body}</p>
                )}

                {isOwner && (
                  <div className="mt-4 space-x-2">
                    <button
                      onClick={() => setIsEditing(true)}
                      className="text-sm text-blue-600 hover:text-blue-800"
                    >
                      Edit
                    </button>
                    <button
                      onClick={handleDeleteQuestion}
                      className="text-sm text-red-600 hover:text-red-800"
                    >
                      Delete Question
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Answers */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          {answers.length} {answers.length === 1 ? 'Answer' : 'Answers'}
        </h2>

        <div className="space-y-4">
          {answers.map((answer) => (
            <AnswerCard key={answer.id} answer={answer} onUpdate={fetchData} />
          ))}
        </div>
      </div>

      {/* Answer Form */}
      {isAuthenticated ? (
        <div className="bg-white p-8 rounded-lg shadow-md">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Your Answer</h3>

          <form onSubmit={handleSubmitAnswer}>
            <textarea
              value={answerBody}
              onChange={(e) => setAnswerBody(e.target.value)}
              rows={6}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Write your answer here..."
            />

            <button
              type="submit"
              disabled={submitting}
              className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {submitting ? 'Posting...' : 'Post Answer'}
            </button>
          </form>
        </div>
      ) : (
        <div className="bg-gray-100 p-6 rounded-lg text-center">
          <p className="text-gray-700">
            Please{' '}
            <button
              onClick={() => navigate('/login')}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              login
            </button>{' '}
            to post an answer
          </p>
        </div>
      )}
    </div>
  );
};

export default QuestionDetail;
