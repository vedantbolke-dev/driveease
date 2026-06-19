# DriveEase System Design Notes

These diagrams were prepared from the actual DriveEase Django project structure and model files.

Files in this folder:
1. `module-diagram.drawio`
2. `er-diagram.drawio`
3. `dfd-level-0.drawio`
4. `dfd-level-1.drawio`
5. `use-case-diagram.drawio`
6. `activity-diagram.drawio`
7. `component-diagram.drawio`
8. `sequence-diagram.drawio`
9. `class-diagram.drawio`

Suggested report captions:
1. `Figure 4.2.1: Module diagram of DriveEase Car Rental System`
2. `Figure 4.2.2: Entity Relationship diagram of DriveEase database`
3. `Figure 4.2.3: Context level DFD of DriveEase system`
4. `Figure 4.2.4: Level 1 DFD of user, car, booking, and admin processes`
5. `Figure 4.2.5: Use case diagram for customer and admin actors`
6. `Figure 4.2.6: Activity diagram for online booking workflow`
7. `Figure 4.2.7: Component diagram of DriveEase architecture`
8. `Figure 4.2.8: Sequence diagram for booking creation`
9. `Figure 4.2.9: Class diagram of core entities and controllers`

Source mapping used:
- `apps/users/models.py`
- `apps/cars/models.py`
- `apps/bookings/models.py`
- `apps/users/views.py`
- `apps/cars/views.py`
- `apps/bookings/views.py`
- `apps/dashboard/views.py`

Recommended use:
- Open each file in Draw.io / diagrams.net.
- Adjust spacing, fonts, or colors only if your college format requires it.
- Export each page as PNG or PDF and place it in the System Design chapter.

Examiner-oriented corrections applied:
- `DFD Level 0` is kept as a true context diagram without internal data stores.
- `ER Diagram` now indicates that `Review` references `Booking`, `User`, and `Car`.
- `Class Diagram` is now model-oriented and does not mix views/controllers with entity classes.
- `CustomUser` inheritance from `AbstractUser` is shown in the class diagram.
- `ContactMessage` remains independent from booking-related model relationships.
