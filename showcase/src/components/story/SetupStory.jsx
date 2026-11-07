import { ArrowUpRight } from 'lucide-react';

export default function SetupStory({ onOpenSetup }) {
  return (
    <section className="story" id="story">
      <div className="story-image">
        <img
          src="/setup.jpg"
          alt="An immersive desktop gaming setup with a large monitor and atmospheric lighting"
          loading="lazy"
        />
        <span className="image-caption">
          A SPACE TO GET LOST. A SETUP TO FIND YOURSELF.
        </span>
      </div>
      <div className="story-copy">
        <h2>
          It’s more than
          <br />a setup.
          <br />
          <span>It’s your space.</span>
        </h2>
        <p>
          Your desk is where the everyday ends and something else begins. Build
          a place that feels as good as the games you play.
        </p>
        <p>
          Start with one piece. Make it yours. The next level isn’t somewhere
          else. It’s right here.
        </p>
        <button className="primary" onClick={onOpenSetup}>
          Build your setup <ArrowUpRight size={18} />
        </button>
        <span className="story-signature">Made for the way you play.</span>
      </div>
    </section>
  );
}
