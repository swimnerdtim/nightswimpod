import EpisodeCard from '../components/EpisodeCard';
import episodes from '../data/episodes.json';
import './Episodes.css';

function Episodes() {
  return (
    <div className="episodes-page">
      <section className="section">
        <div className="container">
          <h1 className="section-title">ALL EPISODES</h1>
          <p className="section-subtitle">
            Dive into our complete library of swimming content. From athlete interviews to training tips.
          </p>
          
          <div className="episodes-count">
            {episodes.length} episode{episodes.length !== 1 ? 's' : ''}
          </div>
          
          <div className="grid-3">
            {episodes.map(episode => (
              <EpisodeCard key={episode.id} episode={episode} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default Episodes;
