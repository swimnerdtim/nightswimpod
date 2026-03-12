import { Link } from 'react-router-dom';
import './EpisodeCard.css';

function EpisodeCard({ episode }) {
  return (
    <Link to={`/episodes/${episode.id}`} className="episode-card card">
      <div className="episode-thumbnail">
        <img src={episode.thumbnail} alt={episode.title} />
        <div className="play-overlay">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="white">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
        {/* Show NEW badge for episodes from last 7 days */}
        {new Date() - new Date(episode.publishDate) < 7 * 24 * 60 * 60 * 1000 && (
          <span className="episode-badge">NEW</span>
        )}
      </div>
      
      <div className="episode-content">
        <p className="episode-date">{new Date(episode.publishDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</p>
        <h3 className="episode-title">{episode.title}</h3>
        <p className="episode-description">{episode.description}</p>
      </div>
    </Link>
  );
}

export default EpisodeCard;
