import { Link } from 'react-router-dom';
import { Question } from '../types';

interface QuestionCardProps {
  question: Question;
}

const QuestionCard = ({ question }: QuestionCardProps) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
      <div className="flex space-x-4">
        {/* Stats */}
        <div className="flex flex-col items-center space-y-2 text-gray-600">
          <div className="text-center">
            <div className="text-xl font-semibold">{question.vote_score}</div>
            <div className="text-xs">votes</div>
          </div>
          <div className="text-center">
            <div className="text-xl font-semibold">{question.answer_count}</div>
            <div className="text-xs">answers</div>
          </div>
          <div className="text-center">
            <div className="text-sm">{question.view_count}</div>
            <div className="text-xs">views</div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1">
          <Link to={`/questions/${question.id}`}>
            <h3 className="text-lg font-semibold text-blue-600 hover:text-blue-800">
              {question.title}
            </h3>
          </Link>

          {question.body && (
            <p className="mt-2 text-gray-700 line-clamp-2">
              {question.body}
            </p>
          )}

          <div className="mt-3 flex items-center justify-between">
            <div className="text-sm text-gray-500">
              Asked by <span className="font-medium">{question.author_username}</span>
            </div>
            <div className="text-sm text-gray-500">
              {formatDate(question.created_at)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionCard;
