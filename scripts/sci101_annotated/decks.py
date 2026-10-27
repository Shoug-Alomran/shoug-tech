"""SCI101 annotated slides — every Introduction to Physical Science chapter deck (Hewitt, Conceptual Physical Science).

The decks carry handwritten working over the slides, so every slide is shown as the original image
(whole=True) and the notes, tips and practice questions sit beside it. Each deck is a namespace class
built by chapter(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def chapter(key, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/math/sci101/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


motion = chapter('d01', 56, "Galileo's concept of inertia, mass as a measure of inertia, net force, the equilibrium rule, weight and support force, friction, speed and velocity, acceleration and free fall.", {
    3: dict(notes=['Inertia: an object’s resistance to a change in its motion (Galileo). Mass is the measure of inertia (kg).'],
            exam=[mcq('Which has more inertia?', ['A 10 kg bowling ball', 'A 1 kg football', 'They are equal', 'Depends on speed'], 0, 'Inertia depends only on mass.')], weight=3),
    14: dict(notes=['Net force: vector sum of all forces. Opposite forces subtract, same-direction forces add.'],
             exam=[mcq('Forces of 10 N east and 4 N west act on a box. The net force is:', ['6 N east', '14 N east', '6 N west', '0'], 0, '')], weight=3),
    17: dict(notes=['Equilibrium rule: ΣF = 0. Static equilibrium (at rest) or dynamic equilibrium (constant velocity).']),
    20: dict(notes=['Weight W = mg (newtons). The support (normal) force balances it on a level surface.']),
    23: dict(notes=['Friction opposes motion (or attempted motion) between surfaces in contact.']),
    30: dict(notes=['Speed = distance/time (scalar); velocity = speed with direction (vector).'],
             exam=[mcq('A car travels 350 m in 10 s. Its average speed is:', ['35 m/s', '3500 m/s', '3.5 m/s', '340 m/s'], 0, '')], weight=3),
    37: dict(notes=['Acceleration a = Δv/Δt (m/s²). Speeding up, slowing down and turning are all acceleration.'],
             tips=[trap('Turning at constant speed is still acceleration: the direction changes.')], weight=3),
    54: dict(notes=['Free fall: a = g ≈ 10 m/s² (9.8). v = gt, d = ½gt².'],
             exam=[mcq('An object falls freely from rest for 3 s. Its speed is about (g = 10 m/s²):', ['30 m/s', '10 m/s', '45 m/s', '90 m/s'], 0, ''),
                   mcq('How far does it fall in those 3 s?', ['45 m', '30 m', '90 m', '15 m'], 0, '½·10·9.')], weight=3),
})

newton = chapter('d02', 19, "Newton's first law (inertia), the second law a = F/m with conceptual and numeric exercises, and the third law: action–reaction pairs acting on different objects.", {
    4: dict(notes=['1st law: an object stays at rest or in uniform straight-line motion unless a net force acts.']),
    5: dict(notes=['2nd law: a = F_net/m. Doubling the force doubles a; doubling the mass halves a.'],
            exam=[mcq('A 75 N net force acts on a 25 kg cart. Its acceleration is:', ['3 m/s²', '1875 m/s²', '0.33 m/s²', '50 m/s²'], 0, '')], weight=3),
    12: dict(notes=['3rd law: whenever A exerts a force on B, B exerts an equal and opposite force on A.'],
             tips=[trap('Action and reaction act on DIFFERENT objects, so they never cancel each other.')],
             exam=[mcq('A boxer hits a punching bag. The force of the bag on the fist is:', ['Equal and opposite to the fist’s force on the bag', 'Smaller', 'Larger', 'Zero'], 0, '')], weight=3),
})

momentum = chapter('d03', 34, 'Momentum and its conservation, energy and work, potential and kinetic energy, the work–energy theorem, conservation of energy, and sources of energy.', {
    2: dict(notes=['Momentum p = mv (vector).']),
    7: dict(notes=['Conservation of momentum: with no external net force, total momentum before = total momentum after.'],
            exam=[short('A 2 kg ball at 3 m/s hits and sticks to a resting 1 kg ball. Find the final speed.', 'p = 2·3 = 6 kg·m/s = (3 kg)·v ⇒ v = 2 m/s.')], weight=3),
    18: dict(notes=['Work W = Fd (joules). Power = work/time.']),
    21: dict(notes=['Potential energy PE = mgh.']),
    22: dict(notes=['Kinetic energy KE = ½mv². Doubling speed quadruples KE.'],
             exam=[mcq('If a car’s speed doubles, its kinetic energy:', ['Quadruples', 'Doubles', 'Halves', 'Stays the same'], 0, '')], weight=3),
    25: dict(notes=['Work–energy theorem: work = ΔKE.']),
    26: dict(notes=['Conservation of energy: energy is not created or destroyed, only transformed (PE ↔ KE).'],
             exam=[mcq('A ball has 500 J of PE at the top. Halfway down (no friction) its KE is:', ['250 J', '500 J', '0 J', '1000 J'], 0, '')], weight=3),
})

gravity = chapter('d04', 16, "Newton's law of universal gravitation, the constant G, the inverse-square law and worked examples.", {
    2: dict(notes=['F = G·m₁m₂/d², G = 6.67 × 10⁻¹¹ N·m²/kg².']),
    7: dict(notes=['Inverse-square law: double the distance → ¼ the force; triple → ⅑.'],
            tips=[trick('Force ∝ 1/d²: 2× farther → 1/4, 3× → 1/9.')],
            exam=[mcq('If the distance between two masses triples, the gravitational force becomes:', ['1/9 as large', '1/3 as large', '3 times larger', '9 times larger'], 0, ''),
                  mcq('If one mass doubles, the force:', ['Doubles', 'Quadruples', 'Halves', 'Stays the same'], 0, '')], weight=3),
})

fluids = chapter('d05', 55, "Density, pressure, liquid pressure with depth, buoyancy and Archimedes' principle, floating and the tip of the iceberg, atmospheric pressure and barometers, and Pascal's principle.", {
    3: dict(notes=['Density ρ = m/V (kg/m³ or g/cm³). Water: 1000 kg/m³ = 1 g/cm³.'],
            exam=[mcq('A 200 g object has a volume of 50 cm³. Its density is:', ['4 g/cm³', '0.25 g/cm³', '10,000 g/cm³', '150 g/cm³'], 0, '')], weight=3),
    12: dict(notes=['Pressure P = F/A (pascals). Smaller area → larger pressure.']),
    17: dict(notes=['Liquid pressure P = ρgh: depends on depth and density, not on the container’s shape.'],
             exam=[mcq('The water pressure 5 m below the surface (ρ = 1000 kg/m³, g = 10 m/s²) is:', ['50,000 Pa', '5,000 Pa', '500 Pa', '50 Pa'], 0, '')], weight=3),
    29: dict(notes=["Archimedes' principle: buoyant force = weight of the fluid displaced (ρ_fluid·V_displaced·g)."],
             tips=[trick('Floats when its density < the fluid’s density; then buoyant force = its weight.')],
             exam=[mcq('An object floats when its density is:', ['Less than the fluid’s density', 'Greater than the fluid’s', 'Equal to 1000 kg/m³ always', 'Zero'], 0, '')], weight=3),
    44: dict(notes=['Atmospheric pressure ≈ 101 kPa at sea level; measured with barometers (mercury: 76 cm).']),
    49: dict(notes=["Pascal's principle: pressure applied to an enclosed fluid is transmitted undiminished everywhere: hydraulic lift F₁/A₁ = F₂/A₂."],
             exam=[short('A hydraulic lift has pistons of area 0.01 m² and 1 m². What force on the small piston lifts 10,000 N?', 'F₁ = F₂·A₁/A₂ = 10,000 × 0.01/1 = 100 N.')], weight=3),
})

thermal = chapter('d06', 15, 'Temperature and its scales, heat as energy in transit, calories and joules, quantity of heat, and specific heat capacity.', {
    2: dict(notes=['Temperature measures the average kinetic energy of the particles. K = °C + 273.']),
    6: dict(notes=['Heat: thermal energy transferred because of a temperature difference (hot → cold).']),
    8: dict(notes=['1 calorie = 4.186 J: the heat to raise 1 g of water by 1 °C.']),
    12: dict(notes=['Q = mcΔT. Water has a very high specific heat (4186 J/kg·°C), so it heats and cools slowly.'],
             exam=[short('How much heat raises 2 kg of water by 10 °C? (c = 4186 J/kg·°C)', 'Q = 2 × 4186 × 10 = 83,720 J.')], weight=3),
})

heat_transfer = chapter('d07', 13, 'Conduction, convection and radiation, wave frequency and temperature, phases of matter, and heat transfer during changes of phase.', {
    2: dict(notes=['Three methods: conduction (collisions, solids), convection (moving fluid), radiation (electromagnetic waves, no medium).'],
            exam=[mcq('A metal spoon heating up in hot soup is mainly:', ['Conduction', 'Convection', 'Radiation', 'Evaporation'], 0, '')], weight=3),
    7: dict(notes=['Convection currents: warm fluid rises, cool fluid sinks.']),
    10: dict(notes=['Hotter objects radiate at higher frequencies (shorter wavelengths).']),
    12: dict(notes=['Phases: solid, liquid, gas, plasma. Melting/boiling absorb energy; freezing/condensing release it, at constant temperature.'],
             tips=[trap('During a phase change the temperature stays constant even though heat is added.')], weight=3),
})

sound = chapter('d08', 23, 'Vibrations and waves (period, frequency, wavelength, speed), the nature of sound, sound waves, reflection (echoes) and refraction of sound.', {
    2: dict(notes=['Wave speed v = fλ; period T = 1/f.'],
            exam=[mcq('A wave with frequency 5 Hz and wavelength 2 m travels at:', ['10 m/s', '2.5 m/s', '0.4 m/s', '7 m/s'], 0, '')], weight=3),
    15: dict(notes=['Sound is a longitudinal mechanical wave (compressions and rarefactions); it needs a medium and can’t travel in a vacuum. ~340 m/s in air.'],
             exam=[tf('Sound can travel through a vacuum.', False, ''),
                   mcq('Sound waves in air are:', ['Longitudinal', 'Transverse', 'Electromagnetic', 'Standing only'], 0, '')], weight=3),
    19: dict(notes=['Reflection of sound = echo.']),
    21: dict(notes=['Refraction: sound bends when its speed changes (e.g. warm vs. cool air layers).']),
})

atoms = chapter('d09', 28, 'Atoms and elements, protons, neutrons and electrons, atomic number and mass, isotopes, the periodic table, electron-dot structures, ions, and ionic, metallic and covalent bonds.', {
    4: dict(notes=['Atomic number Z = number of protons (defines the element). Mass number = protons + neutrons.'],
            exam=[mcq('An atom with 6 protons and 8 neutrons has mass number:', ['14', '6', '8', '2'], 0, '')], weight=3),
    8: dict(notes=['Isotopes: same element (same protons), different numbers of neutrons.'],
            exam=[mcq('Carbon-12 and carbon-14 differ in their number of:', ['Neutrons', 'Protons', 'Electrons', 'Elements'], 0, '')], weight=3),
    10: dict(notes=['Periodic table: rows = periods, columns = groups (similar properties: same number of valence electrons).']),
    16: dict(notes=['Electron-dot structures show valence electrons.']),
    20: dict(notes=['Ions: atoms that lost electrons (positive) or gained them (negative).']),
    21: dict(notes=['Ionic bond: transfer of electrons (metal + nonmetal, e.g. NaCl). Covalent: sharing (nonmetals, e.g. H₂O). Metallic: a "sea" of shared electrons.'],
             tips=[trick('Ionic = give/take; covalent = share; metallic = sea of electrons.')],
             exam=[mcq('The bond in NaCl is:', ['Ionic', 'Covalent', 'Metallic', 'Hydrogen'], 0, ''),
                   mcq('The bonds within an H₂O molecule are:', ['Covalent', 'Ionic', 'Metallic', 'Nuclear'], 0, '')], weight=3),
})

DECKS_HERE = [motion, newton, momentum, gravity, fluids, thermal, heat_transfer, sound, atoms]
