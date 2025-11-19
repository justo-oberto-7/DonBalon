import React from 'react';
import './Home.css';
import Header from '../layout/Header';
import ActionButton from '../shared/ActionButton';

const Home = () => {
  return (
    <div className="home-root">
      <Header />

      <main className="home-hero">
        <div className="hero-content">
          <h1 className="hero-title">DonBalón</h1>
          <p className="hero-sub">Reserva canchas y participa en torneos con la mejor experiencia.</p>

          <div className="hero-ctas">
            <ActionButton onClick={() => console.log('Reservar')} primary>
              Reservar cancha
            </ActionButton>

            <ActionButton onClick={() => console.log('Inscribirse')}>
              Inscribirse a torneos
            </ActionButton>
          </div>
        </div>

        <div className="hero-aside">
          <div className="card">
            <h3>Horarios flexibles</h3>
            <p>Encuentra y reserva el turno que mejor te quede.</p>
          </div>
          <div className="card">
            <h3>Torneos activos</h3>
            <p>Próximamente podrás inscribirte y competir.</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
