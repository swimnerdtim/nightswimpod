import EpisodeCard from '../components/EpisodeCard';
import episodes from '../data/episodes.json';
import './Episodes.css';

function Episodes() {
  // Sort episodes by publish date (newest first)
  const sortedEpisodes = [...episodes].sort((a, b) => 
    new Date(b.publishDate) - new Date(a.publishDate)
  );

  return (
    <div className="episodes-page">
      <section className="section">
        <div className="container">
          <h1 className="section-title">ALL EPISODES</h1>
          <p className="section-subtitle">
            Dive into our complete library of swimming content. From athlete interviews to training tips.
          </p>
          
          <div className="episodes-count">
            {sortedEpisodes.length} episode{sortedEpisodes.length !== 1 ? 's' : ''}
          </div>
          
          <div className="grid-3">
            {sortedEpisodes.map(episode => (
              <EpisodeCard key={episode.id} episode={episode} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default Episodes;
