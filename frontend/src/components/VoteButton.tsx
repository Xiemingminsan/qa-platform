import { useState } from 'react';
import { votesAPI } from '../api/votes';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

interface VoteButtonProps {
  itemId: number;
  itemType: 'question' | 'answer';
  initialScore: number;
  onVote: () => void;
}

const VoteButton = ({ itemId, itemType, initialScore, onVote }: VoteButtonProps) => {
  const { isAuthenticated } = useAuth();
  const [score, setScore] = useState(initialScore);
  const [loading, setLoading] = useState(false);

  const handleVote = async (voteType: 'upvote' | 'downvote') => {
    if (!isAuthenticated) {
      toast.error('Please login to vote');
      return;
    }

    setLoading(true);
    try {
      const response =
        itemType === 'question'
          ? await votesAPI.voteQuestion(itemId, voteType)
          : await votesAPI.voteAnswer(itemId, voteType);

      setScore(response.new_score);
      toast.success(response.message);
      onVote();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to vote');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-1">
      <button
        onClick={() => handleVote('upvote')}
        disabled={loading}
        className="text-gray-400 hover:text-green-600 disabled:opacity-50"
      >
        <svg
          className="w-6 h-6"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      <span className="text-xl font-semibold text-gray-700">{score}</span>

      <button
        onClick={() => handleVote('downvote')}
        disabled={loading}
        className="text-gray-400 hover:text-red-600 disabled:opacity-50"
      >
        <svg
          className="w-6 h-6"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>
    </div>
  );
};

export default VoteButton;
