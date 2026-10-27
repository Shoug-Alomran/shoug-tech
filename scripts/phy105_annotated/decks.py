"""PHY105 annotated slides — every Physics I chapter deck.

The decks mix scanned pages, handwriting and equations, so every slide is shown as the original image
(whole=True) and the notes, tips and practice questions sit beside it. Each deck is a namespace class
built by chapter(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def chapter(key, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/math/phy105/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


KINEMATICS = 'Constant acceleration: v = v₀ + at · x = x₀ + v₀t + ½at² · v² = v₀² + 2a(x − x₀) · x − x₀ = ½(v₀ + v)t. Free fall: a = −g = −9.81 m/s².'

introduction = chapter('d01', 28, 'Physics and its laws, physical quantities (fundamental and derived), SI units and prefixes, rules for writing units, dimensional analysis, unit conversion, scalars vs. vectors and problem solving.', {
    7: dict(notes=['Fundamental (base) quantities: length (m), mass (kg), time (s), plus current, temperature, amount, luminous intensity. Derived quantities combine them (force = kg·m/s² = N).'],
            exam=[mcq('Which is a derived quantity?', ['Force', 'Mass', 'Length', 'Time'], 0, '')], weight=3),
    14: dict(notes=['Dimensional analysis: both sides of a valid equation must have the same dimensions ([L], [M], [T]).'],
             exam=[mcq('The dimensions of acceleration are:', ['[L][T]⁻²', '[L][T]⁻¹', '[M][L][T]⁻²', '[L]²[T]⁻¹'], 0, '')], weight=3),
    24: dict(notes=['Convert units by multiplying by factors equal to 1 (e.g. 1 km/1000 m).'],
             exam=[mcq('72 km/h in m/s is:', ['20 m/s', '72 m/s', '7.2 m/s', '259 m/s'], 0, '72 × 1000 / 3600.')], weight=3),
    25: dict(notes=['Scalars have magnitude only (mass, time, speed); vectors have magnitude and direction (displacement, velocity, force).']),
})

kinematics = chapter('d02', 43, 'Position, distance vs. displacement, average and instantaneous velocity and speed, acceleration, motion with constant acceleration and freely falling objects.', {
    8: dict(notes=['Distance: total path length (scalar). Displacement Δx = x_f − x_i (vector, can be negative or zero).'],
            tips=[trap('A round trip has zero displacement but nonzero distance.')],
            exam=[mcq('You walk 5 m east then 5 m west. Your displacement is:', ['0 m', '10 m', '5 m', '−5 m'], 0, '')], weight=3),
    18: dict(notes=['Average velocity = Δx/Δt; average speed = distance/Δt.']),
    35: dict(notes=[KINEMATICS], tips=[tip(KINEMATICS)],
             exam=[short('A car starts from rest and accelerates at 2 m/s² for 5 s. Find its speed and distance.', 'v = 0 + 2·5 = 10 m/s; x = ½·2·5² = 25 m.')], weight=3),
    37: dict(notes=['Free fall: only gravity acts, a = 9.81 m/s² downward, independent of mass.'],
             exam=[mcq('A ball is dropped from rest. After 2 s its speed is about:', ['19.6 m/s', '9.8 m/s', '4.9 m/s', '39.2 m/s'], 0, '')], weight=3),
})

vectors = chapter('d03', 30, 'Scalars vs. vectors, vector components and direction, adding and subtracting vectors graphically and with components, unit vectors, and the dot and cross products.', {
    10: dict(notes=['Components: Aₓ = A cos θ, A_y = A sin θ. Magnitude A = √(Aₓ² + A_y²), direction θ = tan⁻¹(A_y/Aₓ) (check the quadrant).'],
             exam=[mcq('A 10 m vector at 30° above +x has x-component:', ['8.66 m', '5 m', '10 m', '0.87 m'], 0, '10 cos 30°.')], weight=3),
    12: dict(notes=['Add vectors by adding components: R = (Aₓ + Bₓ) î + (A_y + B_y) ĵ.']),
    17: dict(notes=['Dot product: A·B = AB cos θ = AₓBₓ + A_yB_y + A_zB_z (scalar). Cross product: |A × B| = AB sin θ, direction by the right-hand rule (vector).'],
             tips=[trick('Dot → cos → scalar (zero when perpendicular). Cross → sin → vector (zero when parallel).')],
             exam=[mcq('If A·B = 0 (both nonzero), the vectors are:', ['Perpendicular', 'Parallel', 'Equal', 'Opposite'], 0, '')], weight=3),
})

projectile = chapter('d04', 61, 'Motion in two dimensions, independence of horizontal and vertical motion, projectiles launched horizontally and at an angle, range, maximum height and time of flight.', {
    4: dict(notes=['x and y motions are independent; they share only the time t.']),
    21: dict(notes=['Projectile: aₓ = 0 (constant horizontal velocity), a_y = −g.']),
    25: dict(notes=['Zero launch angle: v₀ₓ = v₀, v₀_y = 0; time to fall h: t = √(2h/g).'],
             exam=[short('A ball rolls off a 1.25 m table at 3 m/s. How far from the table does it land?', 't = √(2·1.25/9.8) ≈ 0.505 s; x = 3 × 0.505 ≈ 1.5 m.')], weight=3),
    32: dict(notes=['General angle: v₀ₓ = v₀ cos θ, v₀_y = v₀ sin θ.']),
    45: dict(notes=['Range (level ground) R = v₀² sin 2θ / g; maximum at θ = 45°. Max height H = v₀² sin²θ / (2g). Time of flight T = 2v₀ sin θ / g.'],
             tips=[trick('Complementary angles (30° and 60°) give the same range.')],
             exam=[mcq('On level ground, which launch angle gives the maximum range?', ['45°', '30°', '60°', '90°'], 0, ''),
                   mcq('At the top of its path a projectile has:', ['Zero vertical velocity but nonzero horizontal velocity', 'Zero velocity', 'Zero acceleration', 'Maximum speed'], 0, '')], weight=3),
})

newton = chapter('d05', 61, "Force and mass, net force, Newton's first law (inertia), mass vs. weight, the second law ΣF = ma, the third law, weight and normal forces, and inclined planes.", {
    9: dict(notes=['Net force = vector sum of all forces. Zero net force ⇒ constant velocity (possibly at rest).']),
    16: dict(notes=["Newton's 1st law (inertia): an object keeps its state of motion unless a net force acts."]),
    22: dict(notes=["Newton's 2nd law: ΣF = ma. 1 N = 1 kg·m/s²."],
             exam=[mcq('A 4 kg box with a net force of 20 N accelerates at:', ['5 m/s²', '80 m/s²', '0.2 m/s²', '24 m/s²'], 0, '')], weight=3),
    43: dict(notes=["Newton's 3rd law: forces come in equal and opposite pairs acting on DIFFERENT objects."],
             tips=[trap('Action–reaction forces never cancel: they act on different bodies.')], weight=3),
    46: dict(notes=['Weight W = mg (a force, in N); mass is the amount of matter (kg), the same everywhere.'],
             exam=[mcq('A 70 kg person’s weight on Earth is about:', ['686 N', '70 N', '70 kg', '7 N'], 0, '')], weight=3),
    50: dict(notes=['Normal force: perpendicular to the surface. On a horizontal surface with no other vertical forces N = mg; on an incline N = mg cos θ.']),
    55: dict(notes=['Incline (frictionless): a = g sin θ down the slope.'],
             exam=[mcq('A block slides down a frictionless 30° incline. Its acceleration is:', ['4.9 m/s²', '9.8 m/s²', '8.5 m/s²', '0'], 0, 'g sin 30°.')], weight=3),
})

friction = chapter('d06', 43, 'Static and kinetic friction and their coefficients, strings (tension) and springs (Hooke’s law), translational equilibrium, and uniform circular motion with centripetal acceleration and force.', {
    6: dict(notes=['Static friction: fₛ ≤ μₛN (adjusts up to a maximum). Kinetic friction: fₖ = μₖN (constant). Usually μₖ < μₛ.'],
            exam=[mcq('A 10 kg box on a floor with μₛ = 0.5. The force needed to start it moving is about:', ['49 N', '98 N', '5 N', '20 N'], 0, '0.5 × 10 × 9.8.')], weight=3),
    21: dict(notes=['Tension pulls along a string. Spring force (Hooke): F = −kx.']),
    28: dict(notes=['Translational equilibrium: ΣFₓ = 0 and ΣF_y = 0.']),
    33: dict(notes=['Uniform circular motion: centripetal acceleration a_c = v²/r toward the centre; net force F_c = mv²/r. Period T = 2πr/v.'],
             tips=[trap('Centripetal force is not a new force: it is the net inward force (tension, friction, gravity…).')],
             exam=[mcq('A 2 kg ball moves at 3 m/s in a circle of radius 1.5 m. The centripetal force is:', ['12 N', '6 N', '4 N', '9 N'], 0, '2·9/1.5.')], weight=3),
})

work = chapter('d07', 54, 'Work done by a constant force W = Fd cos θ, positive and negative work, kinetic energy and the work–energy theorem, work by a variable force (springs), and power.', {
    4: dict(notes=['Work by a constant force: W = Fd cos θ (joules). Positive if the force has a component along the motion, negative if against, zero if perpendicular.'],
            exam=[mcq('Carrying a box horizontally at constant velocity, the work done by your upward holding force is:', ['Zero', 'Positive', 'Negative', 'Equal to mgd'], 0, 'The force is perpendicular to the displacement.')], weight=3),
    32: dict(notes=['Kinetic energy K = ½mv². Work–energy theorem: W_net = ΔK.'],
             exam=[short('How much work is needed to speed a 2 kg cart from 3 m/s to 5 m/s?', 'W = ΔK = ½·2·(25 − 9) = 16 J.')], weight=3),
    40: dict(notes=['Spring: work to stretch by x is ½kx².']),
    42: dict(notes=['Power P = W/t = Fv (watts).'],
             exam=[mcq('Lifting 500 J of work in 10 s requires a power of:', ['50 W', '5000 W', '0.02 W', '510 W'], 0, '')], weight=3),
})

potential = chapter('d08', 46, 'Conservative vs. nonconservative forces, gravitational and spring potential energy, conservation of mechanical energy, and work done by nonconservative forces such as friction.', {
    4: dict(notes=['Conservative force: work is path-independent and zero around a closed path (gravity, springs). Nonconservative: friction, air resistance.'],
            exam=[mcq('Which force is nonconservative?', ['Kinetic friction', 'Gravity', 'Spring force', 'Electrostatic force'], 0, '')], weight=3),
    25: dict(notes=['Gravitational PE U = mgh; spring PE U = ½kx².']),
    30: dict(notes=['Conservation of mechanical energy (conservative forces only): K₁ + U₁ = K₂ + U₂.'],
             exam=[short('A ball is dropped from 5 m. Find its speed just before hitting the ground (ignore air).', 'mgh = ½mv² ⇒ v = √(2gh) = √(2·9.8·5) ≈ 9.9 m/s.')], weight=3),
    39: dict(notes=['With nonconservative forces: W_nc = ΔE = (K₂ + U₂) − (K₁ + U₁) (friction makes it negative).']),
})

momentum = chapter('d09', 46, 'Linear momentum, momentum and Newton’s second law, impulse, conservation of momentum, and inelastic, perfectly inelastic and elastic collisions.', {
    4: dict(notes=['Momentum p = mv (vector, kg·m/s).']),
    13: dict(notes=['Impulse J = FΔt = Δp.'],
             exam=[mcq('A 0.2 kg ball changes from +20 m/s to −20 m/s. The impulse magnitude is:', ['8 N·s', '4 N·s', '0', '40 N·s'], 0, '0.2 × 40.')], weight=3),
    20: dict(notes=['With no net external force, total momentum is conserved: Σp_before = Σp_after.']),
    28: dict(notes=['Inelastic: momentum conserved, kinetic energy NOT. Perfectly inelastic: objects stick: v_f = (m₁v₁ + m₂v₂)/(m₁ + m₂).'],
             exam=[short('A 1000 kg car at 20 m/s hits and sticks to a stopped 1500 kg car. Find the final speed.', 'v = 1000·20/2500 = 8 m/s.')], weight=3),
    33: dict(notes=['Elastic: both momentum and kinetic energy conserved.'],
             tips=[trap('Momentum is conserved in ALL collisions (isolated system); kinetic energy only in elastic ones.')], weight=3),
})

temperature = chapter('d10', 43, 'Temperature and thermal equilibrium (zeroth law), the Celsius, Fahrenheit and Kelvin scales, thermal expansion (linear and volume), and heat transfer by conduction, convection and radiation.', {
    5: dict(notes=['Zeroth law: two objects each in thermal equilibrium with a third are in equilibrium with each other.']),
    13: dict(notes=['T_F = (9/5)T_C + 32; T_K = T_C + 273.15.'],
             exam=[mcq('25 °C equals:', ['77 °F', '45 °F', '298 °F', '57 °F'], 0, ''),
                   mcq('Absolute zero in Celsius is:', ['−273.15 °C', '0 °C', '−100 °C', '−459.67 °C'], 0, '')], weight=3),
    20: dict(notes=['Linear expansion ΔL = αL₀ΔT; volume expansion ΔV = βV₀ΔT, with β ≈ 3α for solids.'],
             exam=[mcq('A 10 m steel rail (α = 1.2 × 10⁻⁵ /°C) warms by 30 °C. It lengthens by:', ['3.6 mm', '0.36 mm', '36 mm', '3.6 m'], 0, '1.2e-5 × 10 × 30 = 3.6e-3 m.')], weight=3),
    35: dict(notes=['Heat transfer: conduction (contact), convection (fluid flow), radiation (electromagnetic waves, no medium needed).'],
             exam=[mcq('Heat from the Sun reaches Earth by:', ['Radiation', 'Conduction', 'Convection', 'Evaporation'], 0, '')], weight=3),
})

DECKS_HERE = [introduction, kinematics, vectors, projectile, newton, friction, work, potential, momentum, temperature]
