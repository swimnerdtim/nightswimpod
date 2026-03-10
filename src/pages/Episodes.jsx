import { useState } from 'react';
import EpisodeCard from '../components/EpisodeCard';
import episodes from '../data/episodes.json';
import './Episodes.css';

function Episodes() {
  const [activeFilter, setActiveFilter] = useState('all');
  
  const filters = [
    { id: 'all', label: 'All' },
    { id: 'hot-takes', label: 'Hot Takes' },
    { id: 'interviews', label: 'Interviews' },
    { id: 'events', label: 'Events' },
    { id: 'training', label: 'Training' },
    { id: 'news', label: 'News' }
  ];
  
  const filteredEpisodes = activeFilter === 'all' 
    ? episodes 
    : episodes.filter(ep => ep.category === activeFilter);

  return (
    <div className="episodes-page">
      <section className="section">
        <div className="container">
          <h1 className="section-title">ALL EPISODES</h1>
          <p className="section-subtitle">
            Dive into our complete library of swimming content. From athlete interviews to training tips.
          </p>
          
          <div className="filter-bar">
            <div className="filter-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z"/>
              </svg>
            </div>
            {filters.map(filter => (
              <button
                key={filter.id}
                className={`filter-button ${activeFilter === filter.id ? 'active' : ''}`}
                onClick={() => setActiveFilter(filter.id)}
              >
                {filter.label}
              </button>
            ))}
          </div>
          
          <div className="episodes-count">
            Showing {filteredEpisodes.length} episode{filteredEpisodes.length !== 1 ? 's' : ''}
          </div>
          
          <div className="grid-3">
            {filteredEpisodes.map(episode => (
              <EpisodeCard key={episode.id} episode={episode} />
            ))}
          </div>
          
          {filteredEpisodes.length === 0 && (
            <div className="no-results">
              <p>No episodes found in this category.</p>
              <button 
                className="btn-primary" 
                onClick={() => setActiveFilter('all')}
              >
                Show All Episodes
              </button>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default Episodes;
