from src.binary_repository.discipline_repo import DisciplineBinaryFileRepository
from src.binary_repository.grade_repo import GradeBinaryFileRepository
from src.binary_repository.student_repo import StudentBinaryFileRepository
from src.repository.discipline_repo import DisciplineRepository
from src.repository.grade_repo import GradeRepository
from src.repository.student_repo import StudentRepository
from src.services.undo_service import UndoService
from src.text_repository.discipline_repo import DisciplineTextFileRepository
from src.text_repository.grade_repo import GradeTextFileRepository
from src.ui.ui import UI

from src.text_repository.student_repo import StudentTextFileRepository

student_repo = StudentRepository()
discipline_repo = DisciplineRepository()
grade_repo = GradeRepository()

# student_repo = StudentTextFileRepository()
# discipline_repo = DisciplineTextFileRepository()
# grade_repo = GradeTextFileRepository()

# student_repo = StudentBinaryFileRepository()
# discipline_repo = DisciplineBinaryFileRepository()
# grade_repo = GradeBinaryFileRepository()


undo_service = UndoService()

console = UI(student_repo, discipline_repo, grade_repo, undo_service)
console.start()
