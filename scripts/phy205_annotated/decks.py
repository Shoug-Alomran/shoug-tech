"""PHY205 annotated slides — every Physics II chapter deck (Halliday, Fundamentals of Physics, 12th ed.).

The equations don't survive text extraction, so every slide is shown as the original image (whole=True)
and the notes, tips and practice questions sit beside it. Each deck is a namespace class built by
chapter(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def chapter(key, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/math/phy205/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


K = 'k = 1/(4πε₀) ≈ 8.99 × 10⁹ N·m²/C², ε₀ = 8.85 × 10⁻¹² C²/(N·m²), e = 1.60 × 10⁻¹⁹ C.'

charge = chapter('d01', 40, "Electric charge, charging by friction, conductors, insulators and semiconductors, polarization and charging by induction, Coulomb's law with multiple forces, and charge quantization and conservation.", {
    6: dict(notes=['Like charges repel, unlike attract. Rubbing transfers electrons: the object that gains electrons becomes negative.']),
    14: dict(notes=['Conductors let charge move freely (metals); insulators don’t (glass, plastic); semiconductors are in between (silicon).']),
    18: dict(notes=['Charging by induction: bring a charged rod near, ground the far side, remove the ground, then the rod: the object keeps the OPPOSITE charge.'],
             exam=[mcq('Charging a neutral sphere by induction with a negative rod leaves the sphere:', ['Positive', 'Negative', 'Neutral', 'Positive then negative'], 0, '')], weight=3),
    23: dict(notes=["Coulomb's law: F = k|q₁||q₂|/r² along the line joining the charges.", K],
             tips=[tip(K), trick('Double r → ¼ the force; double one charge → double the force.')],
             exam=[mcq('Two charges 2 m apart repel with 9 N. At 6 m apart the force is:', ['1 N', '3 N', '27 N', '81 N'], 0, 'Distance ×3 → force ÷9.'),
                   short('Find the force between +3 µC and −2 µC separated by 0.3 m.', 'F = 8.99e9 × 3e-6 × 2e-6 / 0.09 ≈ 0.60 N, attractive.')], weight=3),
    26: dict(notes=['With several charges, add the individual Coulomb forces as VECTORS (superposition).']),
    35: dict(notes=['Charge is quantized: q = ne, n an integer.'],
             exam=[mcq('How many electrons make up −1 C?', ['6.25 × 10¹⁸', '1.6 × 10⁻¹⁹', '9 × 10⁹', '6.02 × 10²³'], 0, '1 / 1.6e-19.')], weight=3),
    38: dict(notes=['Charge is conserved: the net charge of an isolated system never changes (also in pair annihilation/production).']),
})

fields = chapter('d02', 23, 'The electric field as force per unit charge, field lines, the field of point charges and superposition, and the force on a point charge in a field (ink-jet printer).', {
    2: dict(notes=['E = F/q₀ (N/C), pointing in the direction of the force on a POSITIVE test charge.']),
    6: dict(notes=['Field lines: start on + charges, end on − charges, never cross; denser lines = stronger field.'],
            exam=[tf('Electric field lines can cross.', False, '')], weight=3),
    12: dict(notes=['Point charge: E = k|q|/r², away from + and toward −. Several charges: add the field vectors.'],
             exam=[short('Find E 0.5 m from a +2 nC charge.', 'E = 8.99e9 × 2e-9 / 0.25 ≈ 72 N/C, directed away from the charge.')], weight=3),
    20: dict(notes=['F = qE: positive charges are pushed along E, negative charges opposite to E.'],
             tips=[trap('An electron accelerates OPPOSITE to the field direction.')], weight=3),
})

gauss = chapter('d03', 23, "Electric flux through flat and closed surfaces, Gauss' law ε₀Φ = q_enc, its link to Coulomb's law, and charged isolated conductors.", {
    4: dict(notes=['Flux Φ = E·A = EA cos θ (A points out of a closed surface). Flux in counts negative, out positive.']),
    14: dict(notes=["Gauss' law: Φ = ∮E·dA = q_enc/ε₀. Charges outside the surface contribute zero NET flux."],
             exam=[mcq('A closed surface encloses +3q and −q. The net flux is:', ['2q/ε₀', '4q/ε₀', '0', '3q/ε₀'], 0, ''),
                   tf('The net flux through a closed surface depends on charges outside it.', False, '')], weight=3),
    19: dict(notes=['Conductor in electrostatic equilibrium: E = 0 inside, excess charge sits on the outer surface, E just outside is perpendicular to the surface (E = σ/ε₀).'], weight=3),
})

potential = chapter('d04', 39, 'Electric potential energy and potential, work and energy conservation for charges, equipotential surfaces, potential of point charges and groups, finding E from V, potential energy of charge systems, and charged isolated conductors.', {
    7: dict(notes=['V = U/q (volts = J/C). ΔU = qΔV; work by the field W = −ΔU.']),
    11: dict(notes=['Energy conservation: ½mv² gained = |q|ΔV lost. 1 eV = 1.6 × 10⁻¹⁹ J.'],
             exam=[short('A proton is accelerated from rest through 100 V. Find its kinetic energy.', 'K = qΔV = 1.6e-19 × 100 = 1.6 × 10⁻¹⁷ J = 100 eV.')], weight=3),
    16: dict(notes=['Equipotential surfaces are perpendicular to field lines; no work is done moving a charge along one.'],
             exam=[mcq('The work to move a charge along an equipotential surface is:', ['Zero', 'Positive', 'Negative', 'qE'], 0, '')], weight=3),
    25: dict(notes=['Point charge: V = kq/r (a scalar: just add for several charges, with signs).'],
             tips=[trick('Potentials add as numbers; fields add as vectors.')], weight=3),
    27: dict(notes=['E = −dV/ds: the field points toward decreasing potential.']),
    33: dict(notes=['Potential energy of a pair: U = kq₁q₂/r; for a system, sum over every pair.']),
})

capacitance = chapter('d05', 36, 'Capacitance C = q/V, the parallel-plate capacitor, capacitors in series and parallel, energy stored in the electric field, and dielectrics.', {
    3: dict(notes=['C = q/V (farads). Parallel plates: C = ε₀A/d.'],
            exam=[mcq('Doubling the plate separation of a parallel-plate capacitor makes C:', ['Half', 'Double', 'Four times', 'Unchanged'], 0, '')], weight=3),
    9: dict(notes=['Parallel: C_eq = C₁ + C₂ (same V). Series: 1/C_eq = 1/C₁ + 1/C₂ (same q).'],
            tips=[trap('Capacitors combine the OPPOSITE way to resistors.')],
            exam=[mcq('2 µF and 6 µF in series give:', ['1.5 µF', '8 µF', '4 µF', '12 µF'], 0, '')], weight=3),
    20: dict(notes=['Energy U = q²/2C = ½CV² = ½qV; energy density u = ½ε₀E².'],
             exam=[short('A 10 µF capacitor is charged to 12 V. How much energy does it store?', 'U = ½ × 10e-6 × 144 = 7.2 × 10⁻⁴ J.')], weight=3),
    27: dict(notes=['A dielectric multiplies capacitance by κ: C = κC₀ (and reduces the field inside).']),
})

current = chapter('d06', 42, "Electric current and its direction, conservation of charge at junctions, Ohm's law, resistance and resistivity (R = ρL/A), temperature dependence, and power in circuits.", {
    5: dict(notes=['Current i = dq/dt (amperes). Conventional current flows the way positive charge would: opposite to electron motion.']),
    14: dict(notes=['At a junction the current in = current out (charge conservation).']),
    16: dict(notes=["Ohm's law: V = iR, for ohmic materials (linear i–V graph)."]),
    20: dict(notes=['R = ρL/A; resistivity ρ is a material property; conductivity σ = 1/ρ.'],
             exam=[mcq('A wire is stretched to twice its length (same volume). Its resistance becomes:', ['4 times larger', '2 times larger', 'Half', 'Unchanged'], 0, 'L doubles and A halves.')], weight=3),
    28: dict(notes=['Metals: ρ − ρ₀ = ρ₀α(T − T₀): resistance rises with temperature.']),
    32: dict(notes=['Power P = iV = i²R = V²/R (watts).'],
             exam=[mcq('A 1200 W heater runs on 120 V. Its current is:', ['10 A', '144,000 A', '0.1 A', '12 A'], 0, '')], weight=3),
})

circuits = chapter('d07', 69, "EMF and single-loop circuits, internal resistance, potential differences between points, resistors in series and parallel, equivalent resistance examples, and Kirchhoff's junction and loop rules.", {
    5: dict(notes=['An emf device does work on charges to keep a potential difference: ℰ = dW/dq.']),
    11: dict(notes=['With internal resistance r: i = ℰ/(R + r); terminal voltage V = ℰ − ir.'],
             exam=[short('A 12 V battery with r = 0.5 Ω drives a 5.5 Ω resistor. Find i and the terminal voltage.', 'i = 12/6 = 2 A; V = 12 − 2·0.5 = 11 V.')], weight=3),
    14: dict(notes=['Series: R_eq = R₁ + R₂ + … (same current).']),
    18: dict(notes=['Parallel: 1/R_eq = 1/R₁ + 1/R₂ + … (same voltage); R_eq is smaller than the smallest resistor.'],
             exam=[mcq('6 Ω and 3 Ω in parallel give:', ['2 Ω', '9 Ω', '4.5 Ω', '18 Ω'], 0, '')], weight=3),
    35: dict(notes=["Kirchhoff: junction rule Σi_in = Σi_out; loop rule ΣΔV = 0 around any closed loop (−iR in the current's direction, +ℰ going − to +)."],
             tips=[trick('Guess current directions; a negative answer just means the current flows the other way.')], weight=3),
})

magnetism = chapter('d08', 60, "Magnetic fields and field lines, the force on a moving charge F = qv × B and the right-hand rule, circular motion of charges, the force on current-carrying wires, fields from currents (Biot–Savart, Ampère's law), parallel wires, and induction.", {
    5: dict(notes=['Magnetic field lines leave the north pole and enter the south pole; like poles repel.']),
    10: dict(notes=['F = qv × B, magnitude |q|vB sin θ. Zero if v ∥ B. The force is perpendicular to v, so it does no work.'],
             tips=[trap('Use the right-hand rule for a positive charge, then reverse it for an electron.')],
             exam=[mcq('A charge moving parallel to B feels a magnetic force of:', ['Zero', 'qvB', 'Maximum', 'qE'], 0, ''),
                   tf('A magnetic force can change a particle’s speed.', False, 'It only changes direction.')], weight=3),
    16: dict(notes=['Charge in a uniform B moves in a circle: r = mv/(|q|B).']),
    22: dict(notes=['Force on a wire: F = iL × B, magnitude iLB sin θ.'],
             exam=[short('A 2 m wire with 5 A is perpendicular to a 0.3 T field. Find the force.', 'F = iLB = 5 × 2 × 0.3 = 3 N.')], weight=3),
    29: dict(notes=['Long straight wire: B = μ₀i/(2πR), circles around the wire (right-hand grip rule). μ₀ = 4π × 10⁻⁷ T·m/A.']),
    33: dict(notes=["Ampère's law: ∮B·ds = μ₀i_enc."]),
    37: dict(notes=['Parallel currents ATTRACT; antiparallel currents REPEL. F/L = μ₀i₁i₂/(2πd).'],
             exam=[mcq('Two parallel wires carrying current in the same direction:', ['Attract', 'Repel', 'Feel no force', 'Rotate'], 0, '')], weight=3),
    45: dict(notes=["Faraday's law: ℰ = −dΦ_B/dt; Lenz's law: the induced current opposes the change in flux."],
             exam=[mcq('The minus sign in Faraday’s law expresses:', ['Lenz’s law', 'Ampère’s law', 'Gauss’ law', 'Ohm’s law'], 0, '')], weight=3),
})

DECKS_HERE = [charge, fields, gauss, potential, capacitance, current, circuits, magnetism]
