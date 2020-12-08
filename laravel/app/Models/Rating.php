<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Rating extends Model
{
    use HasFactory;

    protected $fillable = [
        'score',
        'comment'
    ];

    protected $casts = [
        'score' => 'float'
    ];

    /**
     * Score mutator
     * @param $score
     */
    public function setScoreAttribute($score)
    {
        if (is_float($score) and $score > 0 and $score <= 5) {
            $this->attributes['score'] = $score;
        }
    }

    /**
     * Comment mutator
     * @param $comment
     */
    public function setCommentAttribute($comment)
    {
        if (is_string($comment) and strlen($comment) <= 100) {
            $this->attributes['comment'] = $comment;
        }
    }
}
