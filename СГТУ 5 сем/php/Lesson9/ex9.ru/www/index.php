<?php
  class Date
  {
    private $year;
    private $month;
    private $day;

    public function __construct($date = null)
    {
      if ($date === null) {
        $date = date('Y-m-d');
      }
      list($this->year, $this->month, $this->day) = explode('-', $date);
    }

    public function getDay()
    {
      return $this->day;
    }

    public function getMonth($lang = null)
    {
      $month = $this->month;
      if ($lang === 'ru') {
        $months = array(
          1 => '������',
          2 => '�������',
          3 => '�����',
          4 => '������',
          5 => '���',
          6 => '����',
          7 => '����',
          8 => '�������',
          9 => '��������',
          10 => '�������',
          11 => '������',
          12 => '�������',
        );
        $month = $months[$this->month];
      } elseif ($lang === 'en') {
        $months = array(
          1 => 'January',
          2 => 'February',
          3 => 'March',
          4 => 'April',
          5 => 'May',
          6 => 'June',
          7 => 'July',
          8 => 'August',
          9 => 'September',
          10 => 'October',
          11 => 'November',
          12 => 'December',
        );
        $month = $months[$this->month];
      }
      return $month;
    }

    public function getYear()
    {
      return $this->year;
    }

    public function getWeekDay($lang = null)
    {
      $day = date('w', strtotime($this->year . '-' . $this->month . '-' . $this->day));
      if ($lang === 'ru') {
        $days = array(
          0 => '�����������',
          1 => '�����������',
          2 => '�������',
          3 => '�����',
          4 => '�������',
          5 => '�������',
          6 => '�������',
        );
        $day = $days[$day];
      } elseif ($lang === 'en') {
        $days = array(
          0 => 'Sunday',
          1 => 'Monday',
          2 => 'Tuesday',
          3 => 'Wednesday',
          4 => 'Thursday',
          5 => 'Friday',
          6 => 'Saturday',
        );
        $day = $days[$day];
      }
      return $day;
    }

    public function addDay($value)
    {
      $this->day += $value;
      $this->normalizeDate();
      return $this;
    }

    public function subDay($value)
    {
      $this->day -= $value;
      $this->normalizeDate();
      return $this;
    }

    public function addMonth($value)
    {
      $this->month += $value;
      $this->normalizeDate();
      return $this;
    }

    public function subMonth($value)
    {
      $this->month -= $value;
      $this->normalizeDate();
      return $this;
    }

    public function addYear($value)
    {
      $this->year += $value;
      return $this;
    }

    public function subYear($value)
    {
      $this->year -= $value;
      return $this;
    }

    public function format($format)
    {
      return date($format, strtotime($this->year . '-' . $this->month . '-' . $this->day));
    }

public function __toString()
  {
    return sprintf('%d-%02d-%02d', $this->year, $this->month, $this->day);
  }

    private function normalizeDate()
    {
      if ($this->day > 31) {
        $this->month += floor($this->day / 31);
        $this->day %= 31;
      }
      if ($this->day < 1) {
        $this->month -= ceil(abs($this->day) / 31);
        $this->day = 31 - abs($this->day) % 31;
      }
      if ($this->month > 12) {
        $this->year += floor($this->month / 12);
        $this->month %= 12;
      }
      if ($this->month < 1) {
        $this->year -= ceil(abs($this->month) / 12);
        $this->month = 12 - abs($this->month) % 12;
      }
    }
  }
?>

<?php
	$date = new Date('2025-12-31');
	
	echo $date->getYear() . "<br>";  // ������� '2025'
	echo $date->getMonth(). "<br>"; // ������� '12'
	echo $date->getDay(). "<br>";   // ������� '31'
	
	echo $date->getWeekDay(). "<br>";     // ������� '3'
	echo $date->getWeekDay('ru'). "<br>"; // ������� '�����'
	echo $date->getWeekDay('en'). "<br>"; // ������� 'wednesday'
?>
<?php
  $date = new Date('2025-12-31');
  $date->addYear(1);
  echo $date . "<br>"; // '2026-12-31'

  $date = new Date('2025-12-31');
  $date->addDay(1);
  echo $date . "<br>"; // '2026-01-01'

  $date = new Date('2025-12-31');
  $date->subDay(3);
  $date->addYear(1);
  echo $date . "<br>"; // '2026-12-28'
?>

