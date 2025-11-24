import { useState } from 'react';
import { Answer } from '../types';
import { useAuth } from '../context/AuthContext';
import { answersAPI } from '../api/answers';
import VoteButton from './VoteButton';
import toast from 'react-hot-toast';

interface AnswerCardProps {
  answer: Answer;
  onUpdate: () => void;
}

const AnswerCard = ({ answer, onUpdate }: AnswerCardProps) => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editBody, setEditBody] = useState(answer.body);
  const [loading, setLoading] = useState(false);

  const isOwner = user && user.username === answer.author_username;

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

  const handleUpdate = async () => {
    if (!editBody.trim()) {
      toast.error('Answer cannot be empty');
      return;
    }

    setLoading(true);
    try {
      await answersAPI.update(answer.id, editBody);
      toast.success('Answer updated');
      setIsEditing(false);
      onUpdate();
    } catch (error) {
      toast.error('Failed to update answer');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this answer?')) return;

    setLoading(true);
    try {
      await answersAPI.delete(answer.id);
      toast.success('Answer deleted');
      onUpdate();
    } catch (error) {
      toast.error('Failed to delete answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex space-x-4">
        {/* Vote buttons */}
        <VoteButton
          itemId={answer.id}
          itemType="answer"
          initialScore={answer.vote_score}
          onVote={onUpdate}
        />

        {/* Content */}
        <div className="flex-1">
          {isEditing ? (
            <div>
              <textarea
                value={editBody}
                onChange={(e) => setEditBody(e.target.value)}
                className="w-full p-3 border rounded-lg"
                rows={4}
              />
              <div className="mt-2 space-x-2">
                <button
                  onClick={handleUpdate}
                  disabled={loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  Save
                </button>
                <button
                  onClick={() => {
                    setIsEditing(false);
                    setEditBody(answer.body);
                  }}
                  disabled={loading}
                  className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <p className="text-gray-800 whitespace-pre-wrap">{answer.body}</p>

              <div className="mt-4 flex items-center justify-between">
                <div className="text-sm text-gray-500">
                  Answered by{' '}
                  <span className="font-medium">{answer.author_username}</span>
                </div>
                <div className="text-sm text-gray-500">
                  {formatDate(answer.created_at)}
                </div>
              </div>

              {isOwner && (
                <div className="mt-3 space-x-2">
                  <button
                    onClick={() => setIsEditing(true)}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    disabled={loading}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnswerCard;
